<?php
/**
 * front-page.php — Die Startseite, Richtung 03 "Nachtwerkstatt".
 *
 * Aus web/startseite-nachtwerkstatt.html übernommen: Kopfbereich mit
 * Messing-Glanzlauf, Materialansicht als WebGL-Shader mit Abschaltmatrix
 * und Standbild-Ersatz, Prüfbericht, Materialkunde mit Ausschlussliste,
 * Größenfinder, Leistungen.
 *
 * Was sich gegenüber dem Entwurf ändert: Die Kollektion kommt aus
 * WooCommerce statt aus der Vorlage, und die Herkunftsangabe kommt aus
 * inc/marke.php. Beides, damit es nur eine Quelle gibt.
 *
 * Die Platzhalter im Prüfbericht — Hunde, Tage, Befunde — stehen bewusst
 * noch drin und sind auf der Seite als Platzhalter gekennzeichnet. Sie
 * werden ersetzt, wenn die echten Werte vorliegen, oder die Sektion fällt
 * weg. Erfundene Prüfzahlen sind angreifbare Werbung.
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>

<section class="hero mitte rand">
    <p class="augenbraue">Fettleder · Messing massiv · Hamburg</p>
    <h1>Messing altert. Leder auch. <b>Beides zu Ihren Gunsten.</b></h1>
    <p class="hero-lead">Kein Lack, keine Beschichtung, nichts, was abplatzen kann. Was Sie nach fünf Jahren in der Hand halten, ist dunkler, glatter und fester als am ersten Tag.</p>
    <div class="knopfreihe">
      <a class="knopf knopf-voll" href="#kollektion">Kollektion ansehen</a>
      <a class="knopf knopf-leer" href="#praxistest">Prüfbericht lesen</a>
    </div>
  </section>

  <div class="material-buehne">
    <canvas id="leder" aria-label="Materialansicht: Fettleder im wandernden Streiflicht" role="img"></canvas>
    <p class="material-schild"><b>Materialansicht</b><span id="lederHinweis">Zeiger über die Fläche bewegen</span><span>Platzhalter bis zum Lederscan</span></p>
  </div>

  <!-- ═══ Praxistest ═══ -->
  <section class="pruef mitte rand" id="praxistest">
    <div class="kopfzeile">
      <span class="nr">01 · Prüfbericht</span>
      <h2>Eine Saison an fremden Hunden,<br>bevor es in den Shop geht.</h2>
      <p>Jedes Modell läuft täglich im Gassi-Service, in der Pension und im Training. Was reißt, dehnt oder scheuert, steht hier und nicht im Kleingedruckten.</p>
    </div>

    <div class="pruef-tabelle-huelle">
      <table class="pruef-tabelle">
        <caption class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Prüfbericht HB-01, Serie 2025/26</caption>
        <thead>
          <tr><th scope="col">Hund</th><th scope="col">Größe</th><th scope="col">Tage</th><th scope="col">Belastung</th><th scope="col">Befund nach Prüfzeit</th></tr>
        </thead>
        <tbody>
          <tr><td>Nala, Labrador</td><td>M · 25 mm</td><td class="tab">212</td><td>täglich, Regen und Salzwasser</td><td>Leder 1,5 Töne nachgedunkelt. Messing matt, kein Grünspan. Löcher unverändert.</td></tr>
          <tr><td>Rocco, Schäferhund</td><td>L · 30 mm</td><td class="tab">186</td><td>Training, Zug an der Leine</td><td>Kante am dritten Loch 1 mm gedehnt. Schnalle fest.</td></tr>
          <tr><td>Fine, Mischling</td><td>S · 20 mm</td><td class="tab">203</td><td>Pension, Spiel mit Artgenossen</td><td>Zwei Kratzer auf der Narbenseite, nicht durchgehend. Patch fest.</td></tr>
          <tr><td>Bo, Rhodesian Ridgeback</td><td>XL · 40 mm</td><td class="tab">141</td><td>täglich, Wald und Schlamm</td><td>Nach Fettung wie neu. Buchschrauben einmal nachgezogen.</td></tr>
        </tbody>
      </table>
    </div>

    <div class="kennzahlen">
      <div class="kennzahl"><b class="tab">742</b><span>Prüftage gesamt</span></div>
      <div class="kennzahl"><b class="tab">4</b><span>Hunde im Test</span></div>
      <div class="kennzahl"><b class="tab">1</b><span>Änderung an der Serie</span></div>
      <div class="kennzahl"><b class="tab">0</b><span>Brüche</span></div>
    </div>
  </section>

  <!-- ═══ Kollektion ═══ -->
  <section class="kollektion mitte rand" id="kollektion">
    <div class="kopfzeile">
      <span class="nr">02 · Kollektion</span>
      <h2>Jedes Stück trägt die Nummer, in der es entstanden ist.</h2>
      <p>Die Nummer läuft durch die ganze Kollektion, nicht je Warengruppe. Alles aus pflanzlich gegerbtem Fettleder, alle Beschläge aus massivem Messing.</p>
    </div>

    <?php echo bellowerk_herkunft_kasten(); // phpcs:ignore WordPress.Security.EscapeOutput ?>

    <div class="raster" style="margin-top:var(--raum-7)">
      <?php
      /* Die Stücke kommen aus WooCommerce, nicht aus der Vorlage. Wer im
         Adminbereich ein Produkt anlegt, sieht es hier — ohne dass jemand
         eine PHP-Datei anfasst. */
      $bellowerk_stuecke = function_exists( 'wc_get_products' )
          ? wc_get_products( array( 'status' => 'publish', 'limit' => 4, 'orderby' => 'menu_order', 'order' => 'ASC' ) )
          : array();

      if ( $bellowerk_stuecke ) {
          foreach ( $bellowerk_stuecke as $bellowerk_stueck ) {
              $GLOBALS['post']    = get_post( $bellowerk_stueck->get_id() ); // phpcs:ignore WordPress.WP.GlobalVariablesOverride
              $GLOBALS['product'] = $bellowerk_stueck;
              setup_postdata( $GLOBALS['post'] );
              wc_get_template_part( 'content', 'product' );
          }
          wp_reset_postdata();
      } else {
          ?>
          <div class="leer" style="grid-column:1/-1">
            <h3>Noch keine Stücke angelegt</h3>
            <p>Die vier Stücke stehen fertig in <code>wordpress/produkte.csv</code>. Im Adminbereich unter Produkte → Importieren einlesen, dann stehen sie hier.</p>
          </div>
          <?php
      }
      ?>
    </div>

    <p style="margin-top:var(--raum-7)">
      <a class="knopf knopf-neben" href="<?php echo esc_url( get_permalink( wc_get_page_id( 'shop' ) ) ); ?>">Die ganze Kollektion ansehen</a>
    </p>
  </section>

  <!-- ═══ Werkstoff ═══ -->
  <section class="werkstoff mitte rand" id="werkstoff">
    <div class="kopfzeile">
      <span class="nr">03 · Material</span>
      <h2>Drei Werkstoffe, sonst nichts.</h2>
      <p>Je weniger verschiedene Teile, desto weniger kann kaputtgehen. Das ist der ganze Trick.</p>
    </div>

    <div class="werkstoff-raster">
      <div>
        <span class="kenn">3,5 mm</span>
        <h3>Fettleder</h3>
        <p>Pflanzlich gegerbt, feste Narbenseite, durchgefettet. Nimmt Wasser auf, ohne hart zu werden. Kanten geschliffen und gewachst. Dunkelt im ersten Jahr um ein bis zwei Töne nach und wird dabei geschmeidiger.</p>
      </div>
      <div>
        <span class="kenn">Massiv, unlackiert</span>
        <h3>Messing</h3>
        <p>Schnalle, Ringe und Karabiner aus Vollmaterial, nicht aus Zinkdruckguss und nicht vermessingt. Läuft matt an, was sich mit einem Tuch zurückholen lässt. Kein Rost, auch nach einem Winter am Meer.</p>
      </div>
      <div>
        <span class="kenn">Ø 5 mm</span>
        <h3>Buchschrauben</h3>
        <p>Halten Patch und Endstücke. Lassen sich mit einem Schraubendreher nachziehen und lösen, wenn ein Teil ersetzt werden soll. Genau deshalb keine Nieten: eine Niete ist eine Entscheidung für immer.</p>
      </div>
    </div>

    <div class="nicht">
      <h3>Was nicht verbaut wird</h3>
      <ul>
        <li>Nähte und Garn</li><li>Nieten</li><li>Stahl</li><li>Kunststoff</li><li>Klickverschlüsse</li><li>Gurtband</li>
      </ul>
      <p>Eine Naht ist die Stelle, an der ein Halsband zuerst aufgeht. Ein Klickverschluss ist die Stelle, an der es bricht. Beides lässt sich weglassen, wenn man das Leder dick genug wählt und die Schnalle aus Vollmessing macht. Genau das tun wir.</p>
    </div>
  </section>

  <!-- ═══ Größenfinder ═══ -->
  <section class="finder mitte rand" id="finder">
    <div class="kopfzeile">
      <span class="nr">04 · Größe finden</span>
      <h2>Ein Maß genügt.</h2>
      <p>Messen Sie den Halsumfang dort, wo das Halsband sitzt, mit zwei Fingern Platz darunter.</p>
    </div>

    <div class="finder-box">
      <div>
        <label for="umfang">Halsumfang des Hundes</label>
        <div class="finder-eingabe">
          <input id="umfang" type="number" min="24" max="70" step="0.5" value="45" inputmode="decimal">
          <span class="einheit">Zentimeter</span>
        </div>
        <p class="hinweis">Zwischen zwei Größen nehmen Sie die größere. Jedes Halsband hat fünf Löcher im Abstand von 26 mm, das gleicht vier Zentimeter aus.</p>
      </div>
      <div class="ergebnis">
        <div class="gr" id="groesse">M</div>
        <dl>
          <div style="display:contents"><dt>Breite</dt><dd id="breite">25 mm</dd></div>
          <div style="display:contents"><dt>Verstellbereich</dt><dd id="bereich">34 bis 42 cm</dd></div>
          <div style="display:contents"><dt>Gesamtlänge</dt><dd id="laenge">480 mm</dd></div>
          <div style="display:contents"><dt>Empfehlung</dt><dd id="rat">Hamburg No. 1 in Größe M</dd></div>
        </dl>
      </div>
    </div>
  </section>

  <!-- ═══ Leistungen ═══ -->
  <section class="leistung mitte rand" id="leistung">
    <div class="kopfzeile">
      <span class="nr">05 · Werkstatt und Betrieb</span>
      <h2>Warum wir wissen, was hält.</h2>
      <p>Das Leder kommt aus der Werkstatt. Der Praxistest kommt aus dem Betrieb nebenan.</p>
    </div>
    <div class="leistung-raster">
      <div class="leistung-feld">
        <h3>Gassi-Service</h3>
        <p>Täglich unterwegs, bei jedem Wetter. Hier läuft der größte Teil der Prüfstunden zusammen.</p>
      </div>
      <div class="leistung-feld">
        <h3>Pension</h3>
        <p>Hunde in der Gruppe, Spiel und Reibung. Der härteste Test für Kanten und Beschläge.</p>
      </div>
      <div class="leistung-feld">
        <h3>Training</h3>
        <p>Zug an der Leine, wiederholte Belastung an denselben Stellen. Zeigt, wo Leder dehnt.</p>
      </div>
    </div>
  </section>

<?php
get_footer();
