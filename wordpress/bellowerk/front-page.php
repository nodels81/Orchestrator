<?php
/**
 * front-page.php — Die Startseite.
 *
 * Stand 13.09.2026: Kopfbereich, Kollektion und Leitidee stehen. Der
 * vollständige Ausbau der Richtung 03 — Materialansicht als WebGL-Shader,
 * Prüfbericht, Größenfinder, Materialkunde — liegt als fertiges HTML in
 * web/startseite-nachtwerkstatt.html und ist noch nicht portiert. Das ist
 * die größte offene Arbeit an diesem Theme.
 */
defined( 'ABSPATH' ) || exit;

get_header();
?>

<section class="hero mitte rand" style="text-align:center;padding-block:clamp(56px,8vw,120px) clamp(36px,5vw,72px)">
  <p class="augenbraue"><?php esc_html_e( 'Fettleder · Messing massiv · Altes Land', 'bellowerk' ); ?></p>
  <h1 style="font-family:var(--display);font-size:var(--step-5);line-height:.99;letter-spacing:-.022em;margin-block:var(--raum-5) 0;max-width:16ch;margin-inline:auto">
    <?php esc_html_e( 'Das Leder wurde vor dem Verkauf', 'bellowerk' ); ?>
    <b class="messing"><?php esc_html_e( 'benutzt', 'bellowerk' ); ?></b>.
  </h1>
  <p style="color:var(--mute);max-width:52ch;margin:var(--raum-6) auto 0">
    <?php esc_html_e( 'Jedes Modell hängt eine Saison an fremden Hunden, bevor es in den Verkauf geht. Täglich, bei jedem Wetter. Was dabei durchfällt, kommt nie in den Katalog.', 'bellowerk' ); ?>
  </p>
  <p style="margin-top:var(--raum-7)">
    <a class="knopf knopf-haupt" href="<?php echo esc_url( get_permalink( wc_get_page_id( 'shop' ) ) ); ?>">
      <?php esc_html_e( 'Die Kollektion ansehen', 'bellowerk' ); ?>
    </a>
  </p>
</section>

<section class="mitte rand" style="padding-block:var(--sektion)">
  <div class="kopfzeile">
    <span class="nr"><?php esc_html_e( '01 · Kollektion', 'bellowerk' ); ?></span>
    <h2><?php esc_html_e( 'Jedes Stück trägt die Nummer, in der es entstanden ist.', 'bellowerk' ); ?></h2>
    <p><?php esc_html_e( 'Die Nummer läuft durch die ganze Kollektion, nicht je Warengruppe. Alles aus pflanzlich gegerbtem Fettleder, alle Beschläge aus massivem Messing.', 'bellowerk' ); ?></p>
  </div>

  <?php echo bellowerk_herkunft_kasten(); // phpcs:ignore WordPress.Security.EscapeOutput ?>

  <div style="margin-top:var(--raum-7)">
    <?php
    if ( function_exists( 'wc_get_products' ) ) {
        $bellowerk_stuecke = wc_get_products(
            array(
                'status'  => 'publish',
                'limit'   => 4,
                'orderby' => 'menu_order',
                'order'   => 'ASC',
            )
        );
        if ( $bellowerk_stuecke ) {
            echo '<div class="raster">';
            foreach ( $bellowerk_stuecke as $bellowerk_stueck ) {
                $GLOBALS['post']    = get_post( $bellowerk_stueck->get_id() ); // phpcs:ignore WordPress.WP.GlobalVariablesOverride
                $GLOBALS['product'] = $bellowerk_stueck;
                setup_postdata( $GLOBALS['post'] );
                wc_get_template_part( 'content', 'product' );
            }
            echo '</div>';
            wp_reset_postdata();
        } else {
            ?>
            <div class="leer">
              <h3><?php esc_html_e( 'Noch keine Stücke angelegt', 'bellowerk' ); ?></h3>
              <p><?php esc_html_e( 'Sobald im Adminbereich Produkte angelegt sind, stehen sie hier. Siehe wordpress/EINRICHTEN.md.', 'bellowerk' ); ?></p>
            </div>
            <?php
        }
    }
    ?>
  </div>
</section>

<?php if ( have_posts() ) : ?>
  <section class="mitte rand rechtsseite" style="padding-block:var(--sektion)">
    <div class="schmal">
      <?php
      while ( have_posts() ) {
          the_post();
          the_content();
      }
      ?>
    </div>
  </section>
<?php endif; ?>

<?php
get_footer();
