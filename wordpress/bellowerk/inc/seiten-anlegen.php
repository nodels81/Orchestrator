<?php
/**
 * seiten-anlegen.php — Legt die Rechtsseiten beim Aktivieren des Themes an.
 *
 * Grund: Fünf lange Rechtstexte von Hand in den Editor zu kopieren ist genau
 * die Stelle, an der ein Absatz verlorengeht und niemand es merkt. Die Texte
 * liegen in inhalte/ und werden hier eingelesen.
 *
 * Vorsichtig: Eine Seite, die es schon gibt, wird NICHT überschrieben. Wer
 * einen Text im Editor geändert hat, verliert die Änderung nicht.
 */

defined( 'ABSPATH' ) || exit;

/** Welche Seiten es gibt: Pfad => [Titel, Datei in inhalte/]. */
function bellowerk_pflichtseiten(): array {
	return array(
		'impressum'              => array( 'Impressum', 'impressum.html' ),
		'datenschutz'            => array( 'Datenschutzerklärung', 'datenschutz.html' ),
		'agb'                    => array( 'Allgemeine Geschäftsbedingungen', 'agb.html' ),
		'widerruf'               => array( 'Widerruf und Rückgabe', 'widerruf.html' ),
		'versand-und-lieferzeit' => array( 'Versand und Lieferzeit', 'versand.html' ),
	);
}

/**
 * Legt fehlende Seiten an. Gibt zurück, was angelegt und was übersprungen wurde.
 */
function bellowerk_seiten_anlegen(): array {
	$bericht = array( 'angelegt' => array(), 'vorhanden' => array(), 'fehlend' => array() );

	foreach ( bellowerk_pflichtseiten() as $pfad => $angaben ) {
		list( $titel, $datei ) = $angaben;

		if ( get_page_by_path( $pfad ) ) {
			$bericht['vorhanden'][] = $titel;
			continue;
		}

		$quelle = get_stylesheet_directory() . '/inhalte/' . $datei;
		if ( ! is_readable( $quelle ) ) {
			$bericht['fehlend'][] = $datei;
			continue;
		}

		$id = wp_insert_post(
			array(
				'post_title'   => $titel,
				'post_name'    => $pfad,
				'post_content' => file_get_contents( $quelle ), // phpcs:ignore WordPress.WP.AlternativeFunctions
				'post_status'  => 'publish',
				'post_type'    => 'page',
				'post_author'  => get_current_user_id() ?: 1,
			),
			true
		);

		if ( is_wp_error( $id ) ) {
			$bericht['fehlend'][] = $titel . ': ' . $id->get_error_message();
		} else {
			$bericht['angelegt'][] = $titel;

			// Datenschutzseite bei WordPress anmelden, damit sie im
			// Anmeldeformular und in den Hinweisen richtig verlinkt wird.
			if ( 'datenschutz' === $pfad ) {
				update_option( 'wp_page_for_privacy_policy', $id );
			}
		}
	}

	return $bericht;
}

/** Beim Aktivieren des Themes einmal laufen lassen. */
function bellowerk_beim_aktivieren(): void {
	$bericht = bellowerk_seiten_anlegen();
	set_transient( 'bellowerk_einrichtung', $bericht, 120 );
}
add_action( 'after_switch_theme', 'bellowerk_beim_aktivieren' );

/** Zeigt einmal an, was passiert ist. */
function bellowerk_einrichtung_melden(): void {
	$bericht = get_transient( 'bellowerk_einrichtung' );
	if ( ! $bericht ) {
		return;
	}
	delete_transient( 'bellowerk_einrichtung' );

	$zeilen = array();
	if ( $bericht['angelegt'] ) {
		$zeilen[] = '<strong>Angelegt:</strong> ' . esc_html( implode( ', ', $bericht['angelegt'] ) );
	}
	if ( $bericht['vorhanden'] ) {
		$zeilen[] = '<strong>Schon vorhanden, nicht angefasst:</strong> ' . esc_html( implode( ', ', $bericht['vorhanden'] ) );
	}
	if ( $bericht['fehlend'] ) {
		$zeilen[] = '<strong>Fehlgeschlagen:</strong> ' . esc_html( implode( ', ', $bericht['fehlend'] ) );
	}
	if ( ! $zeilen ) {
		return;
	}

	printf(
		'<div class="notice notice-%s"><p>%s</p><p><em>%s</em></p></div>',
		$bericht['fehlend'] ? 'error' : 'success',
		wp_kses_post( implode( '<br>', $zeilen ) ),
		esc_html__( 'Die Rechtsseiten sind Entwürfe. Offene Stellen sind im Text orange unterstrichen und müssen vor der Veröffentlichung gefüllt und anwaltlich geprüft werden.', 'bellowerk' )
	);
}
add_action( 'admin_notices', 'bellowerk_einrichtung_melden' );

/**
 * Dauerwarnung, solange eine Pflichtseite fehlt.
 *
 * Ohne Impressum ist der Shop abmahnfähig. Das darf niemand übersehen,
 * deshalb steht der Hinweis, bis er erledigt ist.
 */
function bellowerk_pflichtseiten_pruefen(): void {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$fehlend = array();
	foreach ( bellowerk_pflichtseiten() as $pfad => $angaben ) {
		if ( ! get_page_by_path( $pfad ) ) {
			$fehlend[] = $angaben[0];
		}
	}
	if ( $fehlend ) {
		printf(
			'<div class="notice notice-error"><p><strong>%s</strong> %s</p></div>',
			esc_html__( 'Pflichtseiten fehlen:', 'bellowerk' ),
			esc_html( implode( ', ', $fehlend ) )
		);
	}
}
add_action( 'admin_notices', 'bellowerk_pflichtseiten_pruefen' );
