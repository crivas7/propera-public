# Propera · notificaciones push

## Aspecto

- **iOS:** el sistema usa el icono de la app y el nombre "Propera" automáticamente. Solo controlamos el título, el texto y (opcional) una imagen adjunta.
- **Android:**
  - Icono pequeño: `ic_stat_propera` (halcón blanco sobre transparente; Android lo tiñe). Va en la barra de estado y en la cabecera de la notificación.
  - Color de acento: `@color/notification_accent` = `#7C2CDE` (el lila del splash).

```kotlin
NotificationCompat.Builder(context, CHANNEL_ID)
    .setSmallIcon(R.drawable.ic_stat_propera)
    .setColor(ContextCompat.getColor(context, R.color.notification_accent))
    .setContentTitle(title)
    .setContentText(body)
    .setStyle(NotificationCompat.BigTextStyle().bigText(body))
    .setAutoCancel(true)
```

Si usáis Firebase Cloud Messaging, añadid en el `AndroidManifest.xml`:

```xml
<meta-data android:name="com.google.firebase.messaging.default_notification_icon" android:resource="@drawable/ic_stat_propera" />
<meta-data android:name="com.google.firebase.messaging.default_notification_color" android:resource="@color/notification_accent" />
```

## Tono

- Corto: título de hasta 40 caracteres y texto de hasta 100–110, para que no se corte en la pantalla de bloqueo.
- Siempre con una cifra o un dato útil, nunca un "¡Hola! Entra en la app".
- Honesto: Propera prepara y la persona confirma. Nada de "lo hemos registrado por ti" si no es así.
- Sin alarmismo: informar, no asustar.
- Pocas: como mucho una al día, salvo que la persona active más.

## Catálogo propuesto

| Tipo | Cuándo | Título | Texto |
|---|---|---|---|
| Inicio de mes | Día 1, 9:00 | Nuevo mes, cuentas claras | Hemos reservado tus pagos planificados de {mes} ({total} €). Tu disponible real: {disponible} €. |
| Pago planificado | El día antes, 19:00 | Mañana se cobra {pago} | {importe} € · ya estaba reservado, tu disponible real no cambia. |
| Recordatorio de registro | A diario a la hora elegida (por defecto 21:00), solo si hoy no ha registrado nada | ¿Algo que apuntar hoy? | Díselo a Propera con la voz y solo tendrás que confirmarlo. |
| Sin actividad | Tras 4 días sin movimientos | Llevas {n} días sin registrar | Haz una captura del banco y Propera te prepara los movimientos para revisar. |
| Disponible bajo | Cuando baja de un umbral (p. ej. 50 €) | Te quedan {disponible} € hasta el {fin} | Es tu disponible real, con los pagos planificados ya descontados. |
| Mes cerrado en positivo | Día de cobro o fin de mes, si el saldo es positivo | Mes cerrado en positivo | Te han sobrado {sobrante} € en {mes}. Así se prospera. |

Los valores entre llaves los rellena la app. Los recordatorios de registro y de inactividad deberían poder desactivarse desde los ajustes.
