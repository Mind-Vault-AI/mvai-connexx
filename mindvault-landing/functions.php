<?php
/**
 * Mind Vault AI — Astra Child Theme Functions
 */

// Enqueue parent + child styles
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style('astra-parent', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('mindvault-child', get_stylesheet_uri(), ['astra-parent'], '1.0.0');
});

// Remove default Astra page title on front page
add_filter('astra_the_title', function($title) {
    if (is_front_page()) return '';
    return $title;
});

// Disable Astra header/footer on front page (we have our own)
add_action('wp', function() {
    if (is_front_page()) {
        remove_action('astra_header', 'astra_header_markup');
        remove_action('astra_footer', 'astra_footer_markup');
    }
});
