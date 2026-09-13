<?php
/**
 * page.php — Einzelseiten. Trägt die Rechtsseiten.
 */
defined( 'ABSPATH' ) || exit;
get_header();
?>
<div class="mitte rand rechtsseite" style="padding-block:var(--raum-8) var(--sektion)">
  <div class="schmal">
    <?php while ( have_posts() ) : the_post(); ?>
      <h1><?php the_title(); ?></h1>
      <p class="stand">
        <?php
        printf(
            /* translators: %s: Datum der letzten Änderung */
            esc_html__( 'Stand %s', 'bellowerk' ),
            esc_html( get_the_modified_date( 'd.m.Y' ) )
        );
        ?>
      </p>
      <?php the_content(); ?>
    <?php endwhile; ?>
  </div>
</div>
<?php
get_footer();
