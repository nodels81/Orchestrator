<?php
/**
 * content-product.php — Eine Karte im Katalog.
 */
defined( 'ABSPATH' ) || exit;

global $product;
if ( empty( $product ) || ! $product->is_visible() ) {
    return;
}
$bellowerk_ausverkauft = ! $product->is_in_stock();
?>
<article <?php wc_product_class( 'karte', $product ); ?><?php echo $bellowerk_ausverkauft ? ' data-stand="ausverkauft"' : ''; ?>>

  <?php if ( has_post_thumbnail() ) : ?>
    <a href="<?php the_permalink(); ?>"><?php echo woocommerce_get_product_thumbnail(); // phpcs:ignore ?></a>
  <?php else : ?>
    <a href="<?php the_permalink(); ?>">
      <div class="bildplatz">
        <?php if ( $bellowerk_ausverkauft ) : ?>
          <span class="marke-band"><?php esc_html_e( 'Nicht bestellbar', 'bellowerk' ); ?></span>
        <?php endif; ?>
        <span><?php esc_html_e( 'Noch kein Foto', 'bellowerk' ); ?></span>
      </div>
    </a>
  <?php endif; ?>

  <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>

  <?php if ( $product->get_sku() ) : ?>
    <p class="karte-nr"><?php echo esc_html( $product->get_sku() ); ?></p>
  <?php endif; ?>

  <p><?php echo esc_html( wp_strip_all_tags( $product->get_short_description() ) ); ?></p>

  <div class="karte-fuss">
    <span class="karte-preis tab"><?php echo wp_kses_post( $product->get_price_html() ); ?></span>
    <span class="karte-mehr">
      <?php echo $bellowerk_ausverkauft ? esc_html__( 'Nicht bestellbar', 'bellowerk' ) : esc_html__( 'Ansehen', 'bellowerk' ); ?>
    </span>
  </div>
</article>
