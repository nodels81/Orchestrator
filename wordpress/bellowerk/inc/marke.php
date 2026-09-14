<?php
/**
 * marke.php — Die Markenaussagen an einer Stelle.
 *
 * Grund: Der Herkunftssatz muss auf jeder Produktseite im selben Block wie
 * Preis und Größe stehen (Vorgabe aus konzepte/kollektion-01-hamburg.md).
 * Steht er in jeder Vorlage einzeln, fehlt er irgendwann auf einer. Hier
 * steht er einmal, und jede Vorlage ruft ihn ab.
 *
 * Ändert sich der Fertigungsort für ein Modell, wird unten eine Zeile
 * geändert — nicht zwölf Vorlagen.
 */

defined( 'ABSPATH' ) || exit;

/** Der Herkunftssatz. Stand 12.09.2026. */
function bellowerk_herkunftssatz(): string {
	return __( 'Entworfen, geprüft und gehandelt im Alten Land bei Hamburg. Gefertigt in Deutschland.', 'bellowerk' );
}

/** Derselbe Satz als Kasten für den Preisblock. */
function bellowerk_herkunft_kasten(): string {
	return sprintf(
		'<p class="herkunft"><b>%s</b> &nbsp;%s</p>',
		esc_html__( 'Entworfen, geprüft und gehandelt im Alten Land bei Hamburg.', 'bellowerk' ),
		esc_html__( 'Gefertigt in Deutschland.', 'bellowerk' )
	);
}

/**
 * Fertigungsort je Artikelnummer.
 *
 * Steht bewusst je Artikel und nicht als ein Satz für alles: Sobald ein
 * einziges Modell im Ausland gefertigt wird, ändert sich nur diese eine
 * Zeile, und die Angabe bleibt für alle anderen wahr.
 */
function bellowerk_fertigungsort( string $artikelnummer ): string {
	$orte = array(
		'HB-01'    => 'Harsefeld, Deutschland',
		'LE-01'    => 'Harsefeld, Deutschland',
		'HS-01'    => 'Harsefeld, Deutschland',
		'HB-02'    => 'Harsefeld, Deutschland',
		'LE-02'    => 'Harsefeld, Deutschland',
		'HB-03'    => 'Harsefeld, Deutschland',
		'KO-01'    => 'Harsefeld, Deutschland',
		'PATCH-01' => 'Harsefeld, Deutschland',
	);
	return $orte[ $artikelnummer ] ?? 'Deutschland';
}

/** Verkaufsnamen der Kollektion. Nach außen der Name, intern die Nummer. */
function bellowerk_verkaufsname( string $artikelnummer ): string {
	$namen = array(
		'HB-01' => 'Hamburg No. 1',
		'LE-01' => 'Hamburg No. 2',
		'HS-01' => 'Hamburg No. 3',
		'HB-02' => 'Hamburg No. 4',
		'LE-02' => 'Hamburg No. 5',
		'HB-03' => 'Hamburg No. 6',
		'KO-01' => 'Hamburg No. 7',
	);
	return $namen[ $artikelnummer ] ?? $artikelnummer;
}

/**
 * Werkstoffe, die nicht vorkommen dürfen.
 *
 * Wird beim Speichern eines Produkts geprüft und als Warnung im Adminbereich
 * angezeigt. Kein Verbot — nur ein Hinweis, damit es nicht unbemerkt in einen
 * Produkttext rutscht.
 */
function bellowerk_ausgeschlossene_werkstoffe(): array {
	return array(
		'Naht', 'Nähte', 'genäht', 'Niete', 'Nieten', 'vernietet',
		'Stahl', 'Edelstahl', 'Zinkdruckguss', 'Zamak',
		'Kunststoff', 'Klickverschluss', 'Steckschloss',
		'Gurtband', 'Nylon', 'Paracord',
		'PU-Leder', 'Spaltleder', 'Kunstleder',
		'Geschirr', 'Windhund',
	);
}

/** Pflichtangaben, die in jeder Fußzeile stehen. */
function bellowerk_pflichtzeile(): string {
	return sprintf(
		'%s<br>%s<br>%s',
		esc_html( bellowerk_herkunftssatz() . ' Der Praxistest findet im eigenen Hundebetrieb statt.' ),
		esc_html__( 'Alle Preise inklusive gesetzlicher Umsatzsteuer, zuzüglich Versandkosten. Versandkosten und Lieferzeit siehe Versandseite.', 'bellowerk' ),
		esc_html__( 'Bei Lieferungen außerhalb der EU fallen Zoll und Einfuhrumsatzsteuer des Ziellandes an, die der Besteller trägt.', 'bellowerk' )
	);
}
