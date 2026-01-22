package com.mindvault.mvaiconnexz;

import android.app.Activity;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import android.widget.Toast;

/**
 * MVAI Connexx - Main Activity
 * WebView container voor Flask web applicatie
 *
 * Features:
 * - Laadt https://mvai-connexx.com (of configureerbare URL)
 * - JavaScript enabled voor interactieve features
 * - File upload support
 * - Offline detectie
 * - Progress bar tijdens laden
 * - Back button navigatie binnen app
 */
public class MainActivity extends Activity {

    private WebView webView;
    private ProgressBar progressBar;

    // CONFIGURATIE: Pas deze URL aan voor staging/production
    private static final String APP_URL = "https://mvai-connexx.com";

    // Voor lokale testing: "http://10.0.2.2:5000" (Android emulator → localhost)
    // Voor staging: "https://mvai-connexx.onrender.com"

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialiseer UI components
        webView = findViewById(R.id.webview);
        progressBar = findViewById(R.id.progressBar);

        // Check internet connectie
        if (!isNetworkAvailable()) {
            Toast.makeText(this,
                "Geen internetverbinding. Controleer je netwerk en probeer opnieuw.",
                Toast.LENGTH_LONG).show();
        }

        // WebView configuratie
        configureWebView();

        // Laad applicatie
        webView.loadUrl(APP_URL);
    }

    /**
     * Configureer WebView settings voor optimale performance en security
     */
    private void configureWebView() {
        WebSettings webSettings = webView.getSettings();

        // JavaScript enabled (vereist voor Flask app)
        webSettings.setJavaScriptEnabled(true);

        // DOM Storage enabled (voor login sessies, localStorage)
        webSettings.setDomStorageEnabled(true);

        // Database enabled (voor client-side caching)
        webSettings.setDatabaseEnabled(true);

        // Allow file access voor CSV uploads
        webSettings.setAllowFileAccess(true);

        // Modern rendering
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setUseWideViewPort(true);

        // Caching strategie
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);

        // Zoom controls (disabled - responsive design handelt dit af)
        webSettings.setBuiltInZoomControls(false);
        webSettings.setDisplayZoomControls(false);

        // Mixed content (allow HTTPS + HTTP resources indien nodig)
        // Voor productie: alleen HTTPS!
        webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);

        // WebViewClient - handle page navigatie binnen app
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                // Externe links (Gumroad payment) openen in externe browser
                if (url.contains("gumroad.com") ||
                    url.contains("stripe.com") ||
                    url.contains("paypal.com")) {
                    // Open in system browser voor payment security
                    android.content.Intent intent = new android.content.Intent(
                        android.content.Intent.ACTION_VIEW,
                        android.net.Uri.parse(url)
                    );
                    startActivity(intent);
                    return true;
                }

                // Alle andere links laden binnen WebView
                view.loadUrl(url);
                return true;
            }

            @Override
            public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                progressBar.setVisibility(View.VISIBLE);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                progressBar.setVisibility(View.GONE);
            }

            @Override
            public void onReceivedError(WebView view, int errorCode,
                                       String description, String failingUrl) {
                super.onReceivedError(view, errorCode, description, failingUrl);

                Toast.makeText(MainActivity.this,
                    "Fout bij laden: " + description,
                    Toast.LENGTH_SHORT).show();

                progressBar.setVisibility(View.GONE);
            }
        });

        // WebChromeClient - handle JavaScript dialogs en progress
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                super.onProgressChanged(view, newProgress);
                progressBar.setProgress(newProgress);
            }
        });
    }

    /**
     * Check of device internet heeft (WiFi of mobile data)
     */
    private boolean isNetworkAvailable() {
        ConnectivityManager connectivityManager =
            (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
        return activeNetworkInfo != null && activeNetworkInfo.isConnected();
    }

    /**
     * Back button handling - navigeer binnen WebView history
     */
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    /**
     * Lifecycle - pause WebView bij app minimize
     */
    @Override
    protected void onPause() {
        super.onPause();
        webView.onPause();
    }

    /**
     * Lifecycle - resume WebView bij app restore
     */
    @Override
    protected void onResume() {
        super.onResume();
        webView.onResume();
    }

    /**
     * Cleanup bij destroy
     */
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (webView != null) {
            webView.destroy();
        }
    }
}
