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
    btn.innerHTML = '☣️ Kill Stau';
    btn.style = 'position:fixed;top:10px;right:100px;z-index:9999;background:red;color:white;border-radius:5px;padding:5px;cursor:pointer;';
    document.body.appendChild(btn);

    btn.onclick = () => {
        // Findet alle Fehler-Container und "Something went wrong" Blöcke
        const targets = document.querySelectorAll('.error-message, [data-is-error="true"], .helper-text-container');
        targets.forEach(el => {
            let row = el.closest('.message-row') || el;
            row.remove(); // Entfernt den gesamten Tumor-Block
        });
        console.log('Gee: System-Dissonanz bereinigt, Bre.');
    };
})();