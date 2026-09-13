<?php
/**
 * functions.php — Aufbau des Themes.
 *
 * Hält sich kurz: Was die Marke betrifft, steht in inc/marke.php, was den
 * Shop betrifft, in inc/woocommerce.php. Hier stehen nur Anmeldung und
 * Verdrahtung.
 */

defined( 'ABSPATH' ) || exit;

define( 'BELLOWERK_VERSION', '0.1.0' );

require_once get_stylesheet_directory() . '/inc/marke.php';
require_once get_stylesheet_directory() . '/inc/woocommerce.php';
require_once get_stylesheet_directory() . '/inc/seiten-anlegen.php';

/**
 * Was das Theme kann.
 */
function bellowerk_aufbau(): void {
	load_theme_textdomain( 'bellowerk', get_stylesheet_directory() . '/languages' );

	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );

	// WooCommerce mit eigener Galerie: Zoom und Lightbox laden sonst Skripte,
	// die wir nicht brauchen, und reißen das JavaScript-Budget.
	add_theme_support( 'woocommerce' );
	add_theme_support( 'wc-product-gallery-slider' );

	register_nav_menus(
		array(
			'kopf'  => __( 'Kopfleiste', 'bellowerk' ),
			'fuss'  => __( 'Fußzeile: Kaufen', 'bellowerk' ),
			'recht' => __( 'Fußzeile: Rechtliches', 'bellowerk' ),
		)
	);
}
add_action( 'after_setup_theme', 'bellowerk_aufbau' );

/**
 * Stile und Schriften.
 *
 * ACHTUNG, offener Punkt: Die Schriften sollen im Theme liegen und nicht bei
 * Google — ein Aufruf an fonts.googleapis.com überträgt die IP-Adresse des
 * Besuchers in die USA und braucht dafür eine Einwilligung.
 *
 * Sie liegen aber noch NICHT hier. In assets/ gibt es keine Schriftdateien und
 * kein @font-face. tokens.css verlangt Bodoni Moda, Archivo und IBM Plex Mono,
 * und der Browser fällt auf Georgia und die Systemschrift zurück. Die Seite
 * steht, sieht aber nicht aus wie entworfen.
 *
 * Zu tun: die drei Familien als woff2 nach assets/schriften/ legen und hier
 * per @font-face einbinden. Siehe entscheidungen/offen.md.
 */
function bellowerk_stile(): void {
	$verzeichnis = get_stylesheet_directory();
	$adresse     = get_stylesheet_directory_uri();

	wp_enqueue_style(
		'bellowerk-tokens',
		$adresse . '/assets/tokens.css',
		array(),
		(string) filemtime( $verzeichnis . '/assets/tokens.css' )
	);

	// Themenkopf, damit WordPress das Theme erkennt. Trägt keine Regeln.
	wp_enqueue_style( 'bellowerk-style', get_stylesheet_uri(), array( 'bellowerk-tokens' ), BELLOWERK_VERSION );

	// Die Startseite trägt ihre Sektionen und den Shader selbst — beides
	// lädt nur dort. Auf einer Produktseite wäre es totes Gewicht.
	if ( is_front_page() ) {
		wp_enqueue_style(
			'bellowerk-startseite',
			$adresse . '/assets/startseite.css',
			array( 'bellowerk-tokens' ),
			(string) filemtime( $verzeichnis . '/assets/startseite.css' )
		);
		wp_enqueue_script(
			'bellowerk-startseite',
			$adresse . '/assets/startseite.js',
			array(),
			(string) filemtime( $verzeichnis . '/assets/startseite.js' ),
			true
		);
	}

	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
		wp_enqueue_script( 'comment-reply' );
	}
}
add_action( 'wp_enqueue_scripts', 'bellowerk_stile' );

/**
 * Aufräumen: Was nicht gebraucht wird, wird nicht geladen.
 *
 * Jede dieser Zeilen spart Bytes im ersten Laden. Das Budget aus dem
 * Abnahmetor ist 180 KB JavaScript — WordPress geht ohne Aufräumen locker
 * darüber, bevor eine einzige eigene Zeile geschrieben ist.
 */
function bellowerk_aufraeumen(): void {
	remove_action( 'wp_head', 'wp_generator' );
	remove_action( 'wp_head', 'rsd_link' );
	remove_action( 'wp_head', 'wlwmanifest_link' );
	remove_action( 'wp_head', 'wp_shortlink_wp_head' );
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
	wp_dequeue_style( 'wp-block-library' );
	wp_dequeue_style( 'classic-theme-styles' );
	wp_dequeue_style( 'global-styles' );
}
add_action( 'init', 'bellowerk_aufraeumen' );
add_action( 'wp_enqueue_scripts', 'bellowerk_aufraeumen', 100 );

/**
 * Warnt im Adminbereich, wenn in einem Produkttext ein ausgeschlossener
 * Werkstoff auftaucht.
 *
 * Kein Verbot: Das Wort kann in einer Ausschlussliste völlig richtig stehen
 * ("kommt nicht vor: Nieten"). Es soll nur niemandem unbemerkt durchrutschen.
 */
function bellowerk_werkstoffe_pruefen( int $beitrag_id, WP_Post $beitrag ): void {
	if ( 'product' !== $beitrag->post_type || wp_is_post_revision( $beitrag_id ) ) {
		return;
	}
	$text     = mb_strtolower( $beitrag->post_content . ' ' . $beitrag->post_excerpt );
	$gefunden = array();
	foreach ( bellowerk_ausgeschlossene_werkstoffe() as $wort ) {
		if ( str_contains( $text, mb_strtolower( $wort ) ) ) {
			$gefunden[] = $wort;
		}
	}
	if ( $gefunden ) {
		set_transient( 'bellowerk_werkstoff_warnung_' . $beitrag_id, array_unique( $gefunden ), 60 );
	}
}
add_action( 'save_post', 'bellowerk_werkstoffe_pruefen', 10, 2 );

function bellowerk_werkstoff_hinweis(): void {
	$bildschirm = get_current_screen();
	if ( ! $bildschirm || 'product' !== $bildschirm->post_type ) {
		return;
	}
	$id       = isset( $_GET['post'] ) ? absint( $_GET['post'] ) : 0;
	$gefunden = $id ? get_transient( 'bellowerk_werkstoff_warnung_' . $id ) : false;
	if ( ! $gefunden ) {
		return;
	}
	delete_transient( 'bellowerk_werkstoff_warnung_' . $id );
	printf(
		'<div class="notice notice-warning"><p><strong>%s</strong> %s<br><em>%s</em></p></div>',
		esc_html__( 'Ausgeschlossener Werkstoff im Text:', 'bellowerk' ),
		esc_html( implode( ', ', $gefunden ) ),
		esc_html__( 'Das ist in Ordnung, wenn es in einer Ausschlussliste steht. Sonst gehört es raus — siehe Markenbrief.', 'bellowerk' )
	);
}
add_action( 'admin_notices', 'bellowerk_werkstoff_hinweis' );
