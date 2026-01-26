# GoogleFinanceApp (Android project)
Minimal Android Studio project that opens Google Finance pages inside a WebView.

## How to build APK
1. Download and unzip the project.
2. Open Android Studio -> Open Project -> select the folder `GoogleFinanceApp`.
3. Let Gradle sync. (You may need Android SDK & build tools.)
4. Connect an Android device or start an emulator.
5. Build -> Build Bundle(s) / APK(s) -> Build APK(s).
6. The APK will be in `app/build/outputs/apk/`.

## Note
- This app uses a WebView to display Google Finance. Some pages may restrict embedding or change URL formats.
- For production, consider using a finance API (with proper licensing) and displaying structured data.
