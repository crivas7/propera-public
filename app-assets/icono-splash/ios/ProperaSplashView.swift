import SwiftUI

/// Animación de entrada de Propera. Empieza igual que la pantalla de arranque del sistema
/// (halcón con el ojo vacío) y después: se enciende la pupila, el halcón parpadea y entra "propera.".
/// Llama a `onFinished` al terminar (~1,4 s). Si la app ya está lista antes, puedes cortarla.
struct ProperaSplashView: View {
    var onFinished: () -> Void = {}

    @State private var pupil: CGFloat = 0      // 0 = sin pupila, 1 = pupila completa
    @State private var lid: CGFloat = 0        // 0 = ojo abierto, 1 = cerrado
    @State private var wordmark: Double = 0

    // Posiciones dentro del lienzo de 288 x 288 pt (fracciones 0...1)
    private let pupilAnchor = UnitPoint(x: 0.52, y: 0.4977)
    private let eyeTop: CGFloat = 0.4438
    private let eyeBottom: CGFloat = 0.54

    var body: some View {
        ZStack {
            Color("SplashBackground").ignoresSafeArea()

            ZStack {
                Image("SplashHalcon").resizable()
                ZStack {
                    Image("SplashAnillo").resizable()
                    Image("SplashPupila").resizable()
                        .scaleEffect(pupil, anchor: pupilAnchor)
                }
                .mask(
                    // el párpado sube desde abajo: deja ver solo lo que queda por encima
                    GeometryReader { geo in
                        let visible = eyeBottom - (eyeBottom - eyeTop) * lid
                        VStack(spacing: 0) {
                            Rectangle().frame(height: geo.size.height * visible)
                            Spacer(minLength: 0)
                        }
                    }
                )
            }
            .frame(width: 288, height: 288)

            VStack {
                Spacer()
                Image("SplashMarca")
                    .opacity(wordmark)
                    .offset(y: wordmark == 1 ? 0 : 5)
                    .padding(.bottom, 100)
            }
        }
        .task { await run() }
    }

    private func run() async {
        try? await Task.sleep(for: .milliseconds(150))
        withAnimation(.spring(response: 0.35, dampingFraction: 0.55)) { pupil = 1 }
        try? await Task.sleep(for: .milliseconds(300))
        withAnimation(.easeOut(duration: 0.45)) { wordmark = 1 }
        try? await Task.sleep(for: .milliseconds(400))
        withAnimation(.easeIn(duration: 0.08)) { lid = 1 }          // parpadeo
        try? await Task.sleep(for: .milliseconds(110))
        withAnimation(.easeOut(duration: 0.13)) { lid = 0 }
        try? await Task.sleep(for: .milliseconds(350))
        onFinished()
    }
}

#Preview { ProperaSplashView() }
