<?php
/**
 * footer.php — Fußzeile mit allen Pflichtangaben.
 *
 * Die Rechtslinks stehen hier fest verdrahtet und nicht nur als Menü: Ein
 * Menü kann jemand im Adminbereich leeren, und dann fehlt das Impressum.
 * Das Menü ergänzt, es ersetzt nicht.
 */
defined( 'ABSPATH' ) || exit;

$bellowerk_recht = array(
	'impressum'              => __( 'Impressum', 'bellowerk' ),
	'datenschutz'            => __( 'Datenschutz', 'bellowerk' ),
	'agb'                    => __( 'AGB', 'bellowerk' ),
	'widerruf'               => __( 'Widerruf und Rückgabe', 'bellowerk' ),
	'versand-und-lieferzeit' => __( 'Versand und Lieferzeit', 'bellowerk' ),
);
?>
</main>

<footer class="fuss">
  <div class="mitte rand">
    <div class="fuss-raster">
      <div class="fuss-marke">
        <span class="wortmarke messing"><?php bloginfo( 'name' ); ?></span>
        <p><?php echo esc_html( get_bloginfo( 'description' ) ); ?></p>
      </div>

      <div>
        <h4><?php esc_html_e( 'Kaufen', 'bellowerk' ); ?></h4>
        <?php
        wp_nav_menu(
            array(
                'theme_location' => 'fuss',
                'container'      => false,
                'depth'          => 1,
                'fallback_cb'    => false,
            )
        );
        ?>
      </div>

      <div>
        <h4><?php esc_html_e( 'Werkstatt', 'bellowerk' ); ?></h4>
        <?php
        wp_nav_menu(
            array(
                'theme_location' => 'recht',
                'container'      => false,
                'depth'          => 1,
                'fallback_cb'    => false,
            )
        );
        ?>
      </div>

      <div>
        <h4><?php esc_html_e( 'Rechtliches', 'bellowerk' ); ?></h4>
        <ul>
          <?php foreach ( $bellowerk_recht as $bellowerk_pfad => $bellowerk_titel ) : ?>
            <li><a href="<?php echo esc_url( home_url( '/' . $bellowerk_pfad . '/' ) ); ?>"><?php echo esc_html( $bellowerk_titel ); ?></a></li>
          <?php endforeach; ?>
        </ul>
      </div>
    </div>

    <div class="zahlarten">
      <span><?php esc_html_e( 'PayPal', 'bellowerk' ); ?></span>
      <span><?php esc_html_e( 'Überweisung', 'bellowerk' ); ?></span>
    </div>

    <p class="rechtszeile">
      <?php echo wp_kses_post( bellowerk_pflichtzeile() ); ?>
    </p>
  </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
