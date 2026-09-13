<?php
/**
 * header.php — Kopfleiste und Seitenanfang.
 */
defined( 'ABSPATH' ) || exit;
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<a class="springen" href="#inhalt"><?php esc_html_e( 'Zum Inhalt springen', 'bellowerk' ); ?></a>

<header class="kopf">
  <div class="kopf-innen mitte rand">
    <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="wortmarke messing"><?php bloginfo( 'name' ); ?></a>

    <nav aria-label="<?php esc_attr_e( 'Hauptbereiche', 'bellowerk' ); ?>">
      <?php
      wp_nav_menu(
          array(
              'theme_location' => 'kopf',
              'container'      => false,
              'depth'          => 1,
              'fallback_cb'    => false,
          )
      );
      ?>
    </nav>

    <?php if ( function_exists( 'WC' ) && WC()->cart ) : ?>
      <a class="korb" href="<?php echo esc_url( wc_get_cart_url() ); ?>"
         aria-label="<?php echo esc_attr( sprintf( /* translators: %d: Anzahl */ __( 'Warenkorb, %d Stück', 'bellowerk' ), WC()->cart->get_cart_contents_count() ) ); ?>">
        <?php esc_html_e( 'Warenkorb', 'bellowerk' ); ?> <b><?php echo esc_html( (string) WC()->cart->get_cart_contents_count() ); ?></b>
      </a>
    <?php endif; ?>
  </div>
</header>

<main id="inhalt">
