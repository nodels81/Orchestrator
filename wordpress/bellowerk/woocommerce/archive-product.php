<?php
/**
 * archive-product.php — Der Katalog.
 *
 * Das Werkverzeichnis: Die Nummer läuft durch die ganze Kollektion, nicht je
 * Warengruppe. No. 1 ist das zuerst gebaute Stück, nicht das erste Halsband.
 */
defined( 'ABSPATH' ) || exit;

get_header();
?>

<section class="katalogkopf mitte rand" style="padding-block:var(--raum-9) var(--raum-8);border-bottom:1px solid var(--linie)">
  <p class="augenbraue"><?php esc_html_e( 'Werkverzeichnis', 'bellowerk' ); ?></p>
  <h1 style="font-family:var(--display);font-size:var(--step-4);line-height:1.03;letter-spacing:-.02em;max-width:17ch;margin-block:var(--raum-5)">
    <?php woocommerce_page_title(); ?>
  </h1>
  <?php if ( $bellowerk_beschreibung = get_the_archive_description() ) : ?>
    <div style="color:var(--mute);max-width:56ch"><?php echo wp_kses_post( $bellowerk_beschreibung ); ?></div>
  <?php endif; ?>

  <?php echo bellowerk_herkunft_kasten(); // phpcs:ignore WordPress.Security.EscapeOutput ?>
</section>

<section class="mitte rand">
  <?php if ( woocommerce_product_loop() ) : ?>

    <div class="raster werkraster" style="padding-block:var(--raum-8)">
      <?php
      while ( have_posts() ) {
          the_post();
          do_action( 'woocommerce_shop_loop' );
          wc_get_template_part( 'content', 'product' );
      }
      ?>
    </div>

    <?php do_action( 'woocommerce_after_shop_loop' ); ?>

  <?php else : ?>

    <div class="leer" style="margin-block:var(--raum-8)">
      <h3><?php esc_html_e( 'Nichts in dieser Auswahl', 'bellowerk' ); ?></h3>
      <p><?php esc_html_e( 'In dieser Warengruppe steht zurzeit kein Stück im Verkauf. Die Kollektion wächst langsam, das ist Absicht.', 'bellowerk' ); ?></p>
      <a class="knopf knopf-neben" href="<?php echo esc_url( get_permalink( wc_get_page_id( 'shop' ) ) ); ?>">
        <?php esc_html_e( 'Alles anzeigen', 'bellowerk' ); ?>
      </a>
    </div>

  <?php endif; ?>
</section>

<section class="mitte rand" style="padding-block:var(--raum-7)">
  <div class="meldung meldung-hinweis">
    <div>
      <b><?php esc_html_e( 'Warum hier so wenig steht', 'bellowerk' ); ?></b>
      <p><?php esc_html_e( 'Jedes Stück hängt vor dem Verkauf eine Saison an fremden Hunden. Das dauert, und manches fällt dabei durch.', 'bellowerk' ); ?></p>
    </div>
  </div>
</section>

<?php
get_footer();
