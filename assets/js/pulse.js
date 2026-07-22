/* ============================================================
   PULSE — compteur de visites anonyme, ultra-léger
   Site = 'mullasadra'. Firebase la-voie-du-dedans (analytics seulement).
   Aucune donnée perso, aucun cookie, aucun pistage.
   Même dispositif que jaspers / lessenceretrouvee / lemiroirinterieur.
   ============================================================ */
import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getFirestore, doc, setDoc, increment, serverTimestamp }
  from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

const SITE = 'mullasadra';
const FIRE_CFG = {
  apiKey: "AIzaSyBYlX1AcOP4Yg5rCy9T5tIcrV0WOTT3E24",
  authDomain: "la-voie-du-dedans.firebaseapp.com",
  projectId: "la-voie-du-dedans",
  storageBucket: "la-voie-du-dedans.firebasestorage.app",
  messagingSenderId: "531110328878",
  appId: "1:531110328878:web:322ac57d9504e750b83dbf"
};
const app = getApps().length ? getApps()[0] : initializeApp(FIRE_CFG);
const db = getFirestore(app);

function todayKey(){const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;}
function monthKey(){const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`;}
function normalizePath(p){let s=(p||'/').split('?')[0].split('#')[0];if(/\/$/.test(s)&&/(^|\/)$/.test(s)){}s=s.replace(/^\/+|\/+$/g,'').replace(/\.html?$/,'').replace(/[\/\.]/g,'_');return s.substring(0,80)||'home';}
function deviceKind(){const ua=navigator.userAgent||'';if(/iPad|Tablet|PlayBook|Silk/i.test(ua)||(/Android/i.test(ua)&&!/Mobile/i.test(ua)))return 'tablette';if(/Mobi|iPhone|Android|iPod|Windows Phone/i.test(ua))return 'mobile';return 'ordinateur';}
function langKey(pathKey){return (pathKey==='en'||pathKey.startsWith('en_'))?'en':'fr';}
function zoneKey(){try{const tz=Intl.DateTimeFormat().resolvedOptions().timeZone||'';return tz.replace(/[^A-Za-z0-9]+/g,'_').substring(0,60)||'inconnu';}catch{return 'inconnu';}}

async function pulse(){
  if(/bot|spider|crawler|preview|headless/i.test(navigator.userAgent||''))return;
  const date=todayKey(), month=monthKey(), pathKey=normalizePath(location.pathname);
  const dayUpd={pageviews:increment(1),lastSeen:serverTimestamp()};
  dayUpd[`pages.${pathKey}`]=increment(1);
  try{
    if(localStorage.getItem('pulse_last_day')!==date){
      dayUpd.uniques=increment(1);
      dayUpd[`devices.${deviceKind()}`]=increment(1);
      dayUpd[`langs.${langKey(pathKey)}`]=increment(1);
      dayUpd[`visitors.${localStorage.getItem('pulse_seen')?'back':'new'}`]=increment(1);
      dayUpd[`zones.${zoneKey()}`]=increment(1);
      localStorage.setItem('pulse_seen','1');
      localStorage.setItem('pulse_last_day',date);
    }
  }catch{}
  try{await setDoc(doc(db,'analytics',SITE,'jours',date),dayUpd,{merge:true});}catch(e){console.warn('pulse day',e);}
  const moUpd={pageviews:increment(1)};moUpd[`pages.${pathKey}`]=increment(1);
  try{if(localStorage.getItem('pulse_last_month')!==month){moUpd.uniques=increment(1);localStorage.setItem('pulse_last_month',month);}}catch{}
  try{await setDoc(doc(db,'analytics',SITE,'jours','_mois_'+month),moUpd,{merge:true});}catch(e){console.warn('pulse month',e);}
}
pulse();
