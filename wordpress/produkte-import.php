<?php
/**
 * produkte-import.php — Legt die Artikel aus produkte.csv in WooCommerce an.
 *
 * Wird über "wp eval-file" auf dem Webspace ausgeführt; WordPress und
 * WooCommerce sind dann schon geladen.
 *
 * Warum nicht WC_Product_CSV_Importer: Dessen Spaltenzuordnung entsteht im
 * Adminbereich durch Raten über die Kopfzeile. Ausserhalb des Adminbereichs
 * muss man sie von Hand nachbauen, und ein Tippfehler darin legt stillschweigend
 * ein Produkt ohne Preis an. Hier steht die Zuordnung sichtbar im Code.
 *
 * Läuft mehrfach ohne Schaden: gesucht wird über die Artikelnummer. Ist sie
 * schon da, wird aktualisiert statt ein zweites Mal angelegt.
 */

if ( ! class_exists( 'WooCommerce' ) ) {
	WP_CLI::error( 'WooCommerce ist auf dieser Installation nicht aktiv.' );
}

$datei = '/tmp/bellowerk-produkte.csv';
if ( ! file_exists( $datei ) ) {
	WP_CLI::error( "Datei fehlt: $datei" );
}

$zeiger = fopen( $datei, 'r' );
if ( ! $zeiger ) {
	WP_CLI::error( "Datei nicht lesbar: $datei" );
}

$kopf = fgetcsv( $zeiger );
if ( ! $kopf ) {
	WP_CLI::error( 'Die Datei hat keine Kopfzeile.' );
}
// Die CSV trägt eine Byte-Order-Mark. Bleibt sie stehen, heisst die erste
// Spalte nicht "Type", sondern "\xEF\xBB\xBFType", und nichts passt mehr.
$kopf[0] = preg_replace( '/^\xEF\xBB\xBF/', '', $kopf[0] );

$angelegt     = array();
$aktualisiert = array();
$gescheitert  = array();
$zeile_nr     = 1;

while ( ( $werte = fgetcsv( $zeiger ) ) !== false ) {
	$zeile_nr++;
	if ( count( $werte ) === 1 && trim( (string) $werte[0] ) === '' ) {
		continue;
	}
	if ( count( $werte ) !== count( $kopf ) ) {
		$gescheitert[] = "Zeile $zeile_nr: " . count( $werte ) . ' Felder statt ' . count( $kopf );
		continue;
	}
	$z = array_combine( $kopf, $werte );

	$sku = trim( (string) $z['SKU'] );
	if ( '' === $sku ) {
		$gescheitert[] = "Zeile $zeile_nr: ohne Artikelnummer";
		continue;
	}

	$vorhanden = wc_get_product_id_by_sku( $sku );
	$produkt   = $vorhanden ? wc_get_product( $vorhanden ) : new WC_Product_Simple();
	if ( ! $produkt ) {
		$gescheitert[] = "Zeile $zeile_nr ($sku): Produkt nicht ladbar";
		continue;
	}

	$produkt->set_sku( $sku );
	$produkt->set_name( (string) $z['Name'] );
	$produkt->set_status( '1' === trim( (string) $z['Published'] ) ? 'publish' : 'draft' );
	$produkt->set_featured( '1' === trim( (string) $z['Is featured?'] ) );
	$produkt->set_catalog_visibility( (string) $z['Visibility in catalog'] ?: 'visible' );
	$produkt->set_short_description( (string) $z['Short description'] );
	$produkt->set_description( (string) $z['Description'] );
	$produkt->set_tax_status( (string) $z['Tax status'] ?: 'taxable' );
	$produkt->set_tax_class( (string) $z['Tax class'] );
	$produkt->set_stock_status( '1' === trim( (string) $z['In stock?'] ) ? 'instock' : 'outofstock' );
	$produkt->set_backorders( '1' === trim( (string) $z['Backorders allowed?'] ) ? 'yes' : 'no' );
	$produkt->set_regular_price( (string) $z['Regular price'] );
	$produkt->set_reviews_allowed( '1' === trim( (string) $z['Allow customer reviews?'] ) );
	$produkt->set_menu_order( (int) $z['Position'] );

	// Kategorie: anlegen, falls es sie noch nicht gibt.
	$kategorien = array();
	foreach ( array_filter( array_map( 'trim', explode( ',', (string) $z['Categories'] ) ) ) as $name ) {
		$begriff = get_term_by( 'name', $name, 'product_cat' );
		if ( ! $begriff ) {
			$neu = wp_insert_term( $name, 'product_cat' );
			if ( is_wp_error( $neu ) ) {
				$gescheitert[] = "Zeile $zeile_nr ($sku): Kategorie '$name' — " . $neu->get_error_message();
				continue;
			}
			$kategorien[] = (int) $neu['term_id'];
		} else {
			$kategorien[] = (int) $begriff->term_id;
		}
	}
	if ( $kategorien ) {
		$produkt->set_category_ids( $kategorien );
	}

	// Eigenschaften. Global bedeutet: eine Taxonomie, die sich später filtern
	// laesst. Sonst haengt der Wert nur an diesem einen Artikel.
	$eigenschaften = array();
	for ( $i = 1; $i <= 2; $i++ ) {
		$name = trim( (string) ( $z[ "Attribute $i name" ] ?? '' ) );
		$roh  = trim( (string) ( $z[ "Attribute $i value(s)" ] ?? '' ) );
		if ( '' === $name || '' === $roh ) {
			continue;
		}
		$werte_liste = array_filter( array_map( 'trim', explode( '|', $roh ) ) );
		$sichtbar    = '1' === trim( (string) ( $z[ "Attribute $i visible" ] ?? '1' ) );
		$global      = '1' === trim( (string) ( $z[ "Attribute $i global" ] ?? '0' ) );

		$eigenschaft = new WC_Product_Attribute();
		$eigenschaft->set_name( $name );
		$eigenschaft->set_options( $werte_liste );
		$eigenschaft->set_position( $i - 1 );
		$eigenschaft->set_visible( $sichtbar );
		$eigenschaft->set_variation( false );

		if ( $global ) {
			$taxonomie = wc_attribute_taxonomy_name( $name );
			if ( ! taxonomy_exists( $taxonomie ) ) {
				$id = wc_create_attribute( array( 'name' => $name, 'slug' => sanitize_title( $name ), 'type' => 'select' ) );
				if ( is_wp_error( $id ) ) {
					$gescheitert[] = "Zeile $zeile_nr ($sku): Eigenschaft '$name' — " . $id->get_error_message();
					continue;
				}
				// Die Taxonomie entsteht erst beim naechsten Aufruf von
				// register_taxonomy. Hier von Hand nachholen, sonst greift
				// wp_set_object_terms unten ins Leere.
				register_taxonomy( $taxonomie, 'product', array( 'hierarchical' => false, 'show_ui' => false, 'query_var' => true, 'rewrite' => false ) );
			}
			$begriff_ids = array();
			foreach ( $werte_liste as $wert ) {
				$begriff = get_term_by( 'name', $wert, $taxonomie );
				if ( ! $begriff ) {
					$neu = wp_insert_term( $wert, $taxonomie );
					if ( is_wp_error( $neu ) ) {
						continue;
					}
					$begriff_ids[] = (int) $neu['term_id'];
				} else {
					$begriff_ids[] = (int) $begriff->term_id;
				}
			}
			$eigenschaft->set_id( wc_attribute_taxonomy_id_by_name( $name ) );
			$eigenschaft->set_options( $begriff_ids );
		}
		$eigenschaften[] = $eigenschaft;
	}
	$produkt->set_attributes( $eigenschaften );

	$id = $produkt->save();
	if ( ! $id ) {
		$gescheitert[] = "Zeile $zeile_nr ($sku): Speichern fehlgeschlagen";
		continue;
	}
	if ( $vorhanden ) {
		$aktualisiert[] = "$sku (#$id)";
	} else {
		$angelegt[] = "$sku (#$id)";
	}
}
fclose( $zeiger );

WP_CLI::log( 'angelegt:     ' . ( $angelegt ? implode( ', ', $angelegt ) : '—' ) );
WP_CLI::log( 'aktualisiert: ' . ( $aktualisiert ? implode( ', ', $aktualisiert ) : '—' ) );
if ( $gescheitert ) {
	foreach ( $gescheitert as $zeile ) {
		WP_CLI::warning( $zeile );
	}
	WP_CLI::error( count( $gescheitert ) . ' Zeile(n) nicht eingespielt.' );
}
WP_CLI::success( 'Fertig.' );
