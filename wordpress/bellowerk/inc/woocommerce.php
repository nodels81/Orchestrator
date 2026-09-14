<?php
/**
 * woocommerce.php — Der Shop.
 *
 * Der wichtigste Teil steht gleich oben: Die Herkunftsangabe wird fest in den
 * Preisblock jeder Produktseite gehängt. Vorgabe aus
 * konzepte/kollektion-01-hamburg.md — sie muss so sichtbar sein wie der Name,
 * nicht weggeklappt und nicht nur in der Fußzeile. Hier kann sie niemand
 * vergessen, weil sie nicht in einer Vorlage steht, sondern am Haken hängt.
 */

defined( 'ABSPATH' ) || exit;

/** WooCommerce mit eigener Speicherung der Bestellungen (HPOS). */
add_action(
	'before_woocommerce_init',
	static function (): void {
		if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
			\Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
				'custom_order_tables',
				__FILE__,
				true
			);
		}
	}
);

/**
 * WooCommerce bringt eigene Stile mit. Wir haben ein Designsystem, also
 * fliegen sie raus — sonst kämpfen zwei Systeme um dieselben Elemente.
 */
add_filter( 'woocommerce_enqueue_styles', '__return_empty_array' );

/* ─── Herkunftsangabe in den Preisblock ─────────────────────────────── */

/**
 * Priorität 11 setzt den Satz unmittelbar hinter den Preis (Priorität 10)
 * und vor die Kurzbeschreibung (20). Damit steht er im selben Block wie
 * Preis und Größe, so wie vorgegeben.
 */
function bellowerk_herkunft_ausgeben(): void {
	echo bellowerk_herkunft_kasten(); // phpcs:ignore WordPress.Security.EscapeOutput -- in der Funktion escaped
}
add_action( 'woocommerce_single_product_summary', 'bellowerk_herkunft_ausgeben', 11 );

/**
 * Versandkosten und Lieferzeit stehen vor dem Kaufabschluss auf der
 * Produktseite, nicht erst im Kassenbereich. Das ist Vorschrift und
 * gleichzeitig der häufigste Grund für abgebrochene Käufe.
 */
function bellowerk_versandhinweis(): void {
	$seite = get_page_by_path( 'versand-und-lieferzeit' );
	$link  = $seite ? get_permalink( $seite ) : home_url( '/versand-und-lieferzeit/' );
	printf(
		'<p class="steuerzeile">%s <a href="%s">%s</a>.<br>%s</p>',
		esc_html__( 'Inklusive 19 % Umsatzsteuer, zuzüglich', 'bellowerk' ),
		esc_url( $link ),
		esc_html__( 'Versandkosten', 'bellowerk' ),
		esc_html__( 'Versand innerhalb Deutschlands 4,90 €, ab 120 € versandkostenfrei. Lieferzeit 2 bis 4 Werktage.', 'bellowerk' )
	);
}
add_action( 'woocommerce_single_product_summary', 'bellowerk_versandhinweis', 12 );

/* ─── Artikelnummer sichtbar halten ─────────────────────────────────── */

/**
 * Der Name steht groß, die Artikelnummer klein darunter in Mono. Beide
 * müssen auffindbar sein, weil Bestandskunden nach HB-01 suchen werden.
 */
function bellowerk_artikelnummer(): void {
	global $product;
	if ( ! $product instanceof WC_Product ) {
		return;
	}
	$nummer = $product->get_sku();
	if ( $nummer ) {
		printf( '<p class="artikelnr">%s</p>', esc_html( $nummer ) );
	}
}
add_action( 'woocommerce_single_product_summary', 'bellowerk_artikelnummer', 6 );

/* ─── Aufräumen ─────────────────────────────────────────────────────── */

// Die Bewertungssterne im Katalog fliegen raus, solange es keine
// Bewertungen gibt. Eine leere Sternreihe sieht aus wie null Sterne.
remove_action( 'woocommerce_after_shop_loop_item_title', 'woocommerce_template_loop_rating', 5 );

// Die Ergebnisanzahl und die Sortierung im Katalog: bei sieben Stücken Unfug.
remove_action( 'woocommerce_before_shop_loop', 'woocommerce_result_count', 20 );
remove_action( 'woocommerce_before_shop_loop', 'woocommerce_catalog_ordering', 30 );

// Verwandte Produkte: bei einer Kollektion aus sieben Stücken ist "das
// könnte dir auch gefallen" albern. Der Katalog steht einen Klick entfernt.
remove_action( 'woocommerce_after_single_product_summary', 'woocommerce_output_related_products', 20 );

/** Vier Karten je Reihe, wie im Entwurf. */
add_filter( 'loop_shop_columns', static fn(): int => 4 );

/** Alle sieben Stücke auf eine Seite. Eine Kollektion blättert man nicht. */
add_filter( 'loop_shop_per_page', static fn(): int => 24, 20 );

/* ─── Bestellknopf und Pflichttexte ─────────────────────────────────── */

/**
 * Der Bestellknopf muss "Zahlungspflichtig bestellen" heißen (§ 312j BGB).
 * WooCommerce schreibt standardmäßig "Jetzt kaufen" — das genügt nicht.
 */
add_filter(
	'woocommerce_order_button_text',
	static fn(): string => __( 'Zahlungspflichtig bestellen', 'bellowerk' )
);

/**
 * Hinweis auf Zoll und Einfuhrsteuer im Warenkorb, sobald ein Ziel außerhalb
 * der EU gewählt ist. Steht dann dort, wo die Entscheidung fällt.
 */
function bellowerk_drittland_hinweis(): void {
	$land = WC()->customer ? WC()->customer->get_shipping_country() : '';
	if ( ! $land || bellowerk_ist_eu( $land ) ) {
		return;
	}
	wc_print_notice(
		esc_html__( 'Lieferung außerhalb der EU: Zoll und Einfuhrumsatzsteuer des Ziellandes kommen hinzu und werden dort erhoben, nicht von uns. Sie trägt der Besteller.', 'bellowerk' ),
		'notice'
	);
}
add_action( 'woocommerce_before_cart', 'bellowerk_drittland_hinweis' );
add_action( 'woocommerce_before_checkout_form', 'bellowerk_drittland_hinweis' );

/** Länder der Europäischen Union. */
function bellowerk_ist_eu( string $land ): bool {
	$eu = array(
		'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR',
		'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL',
		'PT', 'RO', 'SE', 'SI', 'SK',
	);
	return in_array( strtoupper( $land ), $eu, true );
}

/**
 * Keine erfundene Knappheit. WooCommerce blendet "Nur noch 2 auf Lager" ein,
 * sobald der Bestand geführt wird — das ist nur dann zulässig, wenn es
 * stimmt. Wir zeigen es, aber ohne Drängeln im Text.
 */
add_filter(
	'woocommerce_get_availability_text',
	static function ( string $text, WC_Product $produkt ): string {
		if ( ! $produkt->is_in_stock() ) {
			return __( 'Zurzeit nicht auf Lager. Auf Anfrage als Anfertigung.', 'bellowerk' );
		}
		return $text;
	},
	10,
	2
);
