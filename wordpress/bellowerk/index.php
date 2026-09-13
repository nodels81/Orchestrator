<?php
/**
 * index.php — Auffangvorlage. WordPress verlangt sie.
 */
defined( 'ABSPATH' ) || exit;
get_header();
?>
<div class="mitte rand" style="padding-block:var(--raum-8) var(--sektion)">
  <?php if ( have_posts() ) : ?>
    <div class="kopfzeile">
      <h2><?php echo esc_html( get_the_archive_title() ?: get_bloginfo( 'name' ) ); ?></h2>
    </div>
    <?php while ( have_posts() ) : the_post(); ?>
      <article class="schmal" style="margin-bottom:var(--raum-8)">
        <h3 style="font-family:var(--display);font-size:var(--step-2)">
          <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
        </h3>
        <div style="color:var(--mute)"><?php the_excerpt(); ?></div>
      </article>
    <?php endwhile; ?>
    <?php the_posts_pagination(); ?>
  <?php else : ?>
    <div class="leer">
      <h3><?php esc_html_e( 'Hier ist nichts', 'bellowerk' ); ?></h3>
      <p><?php esc_html_e( 'Diese Seite gibt es nicht oder nicht mehr. Die Kollektion ist überschaubar — das ist der schnellste Weg zurück.', 'bellowerk' ); ?></p>
      <a class="knopf knopf-haupt" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Zur Startseite', 'bellowerk' ); ?></a>
    </div>
  <?php endif; ?>
</div>
<?php
get_footer();
