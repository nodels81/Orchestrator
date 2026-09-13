<?php
/**
 * single-product.php — Die Produktseite.
 *
 * Der Aufbau folgt dem Entwurf: Galerie links, Kaufblock rechts, darunter
 * Praxistest, Maße und Material, Fragen.
 *
 * Die Herkunftsangabe steht NICHT in dieser Datei, sondern hängt in
 * inc/woocommerce.php am Haken woocommerce_single_product_summary. Absicht:
 * So kann sie beim Ändern einer Vorlage nicht verlorengehen.
 */
defined( 'ABSPATH' ) || exit;

get_header();

while ( have_posts() ) :
    the_post();
    global $product;
    ?>

    <nav class="brot mitte rand" aria-label="<?php esc_attr_e( 'Sie sind hier', 'bellowerk' ); ?>"
         style="font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);padding-block:var(--raum-6) 0">
      <?php woocommerce_breadcrumb( array( 'delimiter' => ' <span style="color:var(--linie-hell)">/</span> ' ) ); ?>
    </nav>

    <div id="product-<?php the_ID(); ?>" <?php wc_product_class( 'produkt mitte rand', $product ); ?>
         style="display:grid;grid-template-columns:1.15fr .85fr;gap:var(--raum-9);padding-block:var(--raum-7) var(--sektion);align-items:start">

      <div class="galerie-haupt">
        <?php
        /**
         * Galerie. Ohne Bild steht die Aufnahmeanweisung da — solange keine
         * echten Fotos vorliegen, ist eine leere Fläche ehrlicher als ein
         * Platzhalterbild, das nach Produkt aussieht.
         */
        if ( has_post_thumbnail() ) {
            do_action( 'woocommerce_before_single_product_summary' );
        } else {
            printf(
                '<div class="bildplatz" style="aspect-ratio:4/5"><span>%s<br><br>%s</span></div>',
                esc_html__( 'Noch kein Foto', 'bellowerk' ),
                esc_html__( 'Aufnahmeanweisung siehe web/aufnahmen/', 'bellowerk' )
            );
        }
        ?>
      </div>

      <div class="kaufblock">
        <?php
        /**
         * Reihenfolge im Kaufblock, nach Priorität:
         *   5 Titel · 6 Artikelnummer · 10 Preis · 11 HERKUNFT · 12 Versand
         *   20 Kurzbeschreibung · 30 Kaufen · 40 Meta
         */
        do_action( 'woocommerce_single_product_summary' );
        ?>
      </div>
    </div>

    <?php
    /* Beschreibung, Maße, weitere Reiter — unterhalb des Kaufblocks. */
    do_action( 'woocommerce_after_single_product_summary' );
    ?>

    <section class="abschnitt mitte rand" style="padding-block:var(--sektion)">
      <div class="schmal">
        <div class="leer">
          <h3><?php esc_html_e( 'Noch keine Bewertungen', 'bellowerk' ); ?></h3>
          <p><?php esc_html_e( 'Hier stehen später echte Kundenstimmen mit Foto — und nur echte. Bis dahin bleibt die Fläche leer.', 'bellowerk' ); ?></p>
        </div>
      </div>
    </section>

    <?php
endwhile;

get_footer();
