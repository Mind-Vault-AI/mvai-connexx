# MVAI Connexx - ProGuard Rules
# Code obfuscation voor release builds

# Keep WebView JavaScript interface
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep activity
-keep public class com.mindvault.mvaiconnexz.MainActivity {
    public *;
}

# WebView debugging
-keepattributes JavascriptInterface
-keepattributes *Annotation*

# Keep line numbers voor crash reports
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# Optimization
-optimizationpasses 5
-dontusemixedcaseclassnames
-dontskipnonpubliclibraryclasses
-verbose
