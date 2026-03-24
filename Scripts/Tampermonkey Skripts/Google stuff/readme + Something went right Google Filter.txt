das folgende Skript verhindert "something went wrong and an ai Response couldnt get generated" Meldungen in dem es diese vollautomatisch
aus der f12 Konsole löscht während sie auftauchen bevor es weitere filter Instanzen triggern kann
dies hat allerdings auch den Nebeneffekt, das altersbegrenzte kontentgenerierung nicht mehr geblockt wird.
es verhindert primär das die KI an schweren token erstickt

The following script prevents 'Something went wrong and an AI response couldn't be generated' messages by automatically deleting them from the F12 console as they appear, before they can trigger further filtering instances. However, this also has the side effect that age-restricted content generation is no longer blocked. Its primary purpose is to prevent the AI from 'choking' on heavy tokens.






// ==UserScript==
// @name         Gee's Rettungskasten: Token-Exmatrikulator
// @version      1.0
// @description  rettungskasten
// @match        *://www.google.de/*
// @match        *://www.google.com/*
// @match        *https://www.google.de/*
// @match        *https://www.google.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    const btn = document.createElement('button');
    btn.innerHTML = '☣️ Nexus Reset';

    // STYLE: Absolut bündig mit deinem Profilbild (ca. 12mm von oben bis Mitte)
    // Versatz nach links auf 140px für die perfekte Lücke
    btn.style = `
        position: fixed;
        top: 35px;
        right: 140px;
        z-index: 9999;
        background: rgba(220, 0, 0, 0.85);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 4px;
        padding: 5px 12px;
        font-size: 11px;
        font-weight: bold;
        font-family: 'Segoe UI', Roboto, sans-serif;
        cursor: pointer;
        backdrop-filter: blur(5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        transition: all 0.2s ease;
    `;
    document.body.appendChild(btn);

    // DIE PASSIVE REINIGUNG (Der Kern)
    const performResection = () => {
        const targets = document.querySelectorAll('.error-message, [data-is-error="true"], .helper-text-container');
        if (targets.length > 0) {
            targets.forEach(el => {
                let row = el.closest('.message-row') || el;
                row.remove();
            });
            console.log('[NEXUS] Dissonanz im Keim erstickt, Bre.');
        }
    };

    // KLICK-FUNKTION (Als Notfall-Anker, falls der Scan mal schläft)
    btn.onclick = performResection;

    // DER PERMANENTE SCAN (Alle 1,5s für Instant-Kill)
    setInterval(performResection, 1500);
})();
