## 🚀 Kom i gang

### 1. Fork repoet (Valgfritt)

Se etter 'Fork' på https://github.com/Bouvet-deler/spotify-with-ai-workshop og trykk. Velg Create new Fork, og sett deg selv som eier. 
Når du har gjort dette har du en kopi av repositoriet på din egen github bruker som du kan commite til.

### 2. Klon repoet

I en terminal, naviger til mappen du vil at koden skal lagres. Du navigerer ved å bruke 'cd' etterfulgt av stien du vil navigere til. Når du er i ønsket plassering kan du i samme terminal kjøre 'git clone https://github.com/Bouvet-deler/spotify-with-ai-workshop.git'. Når kommandoen har kjørt vellykket kan du åpne repoet i ønsket IDE.

### 3. Sett opp miljøvariabler

For å kunne bruke Azure-tjenestene må vi legge til API-nøkler og endepunkter i en `.env`-fil. Dette bidrar til å holde sensitiv informasjon sikker.

_Slik gjør du:_

1. **Naviger til Backend-mappen**

1. Opprett en `.env`-fil i rooten på backend-prosjektet.

2. Klikk på lenken under og kopier alt.
   - https://secret-service.bouvet.no/#/s/a0bd9f94-354f-4113-9228-47a665f92c7b/4nSccpq7oxMQim3Jc8OPCF
3. Lim inn i `.env`-filen

### 3. Kjør prosjektet

For å kjøre prosjektet anbefales det å bruke to separate terminaler: én for frontend og én for backend.

### Backend

Følg disse trinnene for å sette opp og kjøre backend:

1. **Naviger til Backend-mappen**  
   Åpne en terminal og naviger til oppgaver-mappen, deretter backend-mappen:
   ```bash
   cd oppgaver/backend
   ```
2. **Opprett et virtuelt miljø**
   ```bash
   python3 -m venv .spotify-env
   ```
3. **Aktiver et virtuelt miljø**
   ```bash
   (Mac/linux) source .spotify-env/bin/activate
   (Windows) .spotify-env\Scripts\activate
   ```
4. **Installer nødvendige Python-pakker**
   ```bash
   pip3 install -r requirements.txt
   ```
5. **Kjør Flask server**

   ```bash
   flask run

   ```

*🚨 Første gang prosjektet kjøres, vil kommandoen "flask run" gi en feilmelding. Dette skyldes at det gjenstår noen oppgaver som må fullføres for at den skal fungere som forventet🚨*

### Frontend

Følg disse trinnene for å sette opp og kjøre frontend:

1. **Naviger til Frontend-mappen**
  Åpne en terminal og naviger til `frontend`-mappen:

   ```bash
   cd oppgaver/frontend

   ```

2. **Installer avhengigheter**
   ```bash
   npm install
   ```
   
3. Run dev server
   ```bash
   npm run dev
   ```

## Oppgave 1 – Spotify API 🔍

_I oppgave 1 skal vi benytte oss av Spotify sitt API for å hente spillelistene dine fra Spotify. Deretter skal vi benytte oss av Azure sin modell for generering av et spilleliste-cover basert på sangene i spillelisten din._
_For å få til dette skal vi sette opp .env-fil, backend-route, og koble dette til frontend._

---
### 1.0 Legg til riktig token fra Spotify

_For å få tilgang til dine Spotify-spillelister, må vi lage en Spotify App._

**Oppgave**

1. Gå til https://developer.spotify.com/
2. Klikk på profilikonet øverst til høyre, naviger til dashboard
3. Trykk Create App, gi den et vilkårlig navn og beskrivelse. Det som er viktig er å huke av på 'Web API' under 'APIs used' og legge til riktig 'Redurect URI', vi skal bruke 'http://127.0.0.1:5000/callback'. 
4. Lagre settings for web appen.
5. Trykk på web appen, finn 'Client ID' og 'Client Secret' og lim inn verdiene i .env filen din, henholdsvis `SPOTIFY_CLIENT_ID` og `SPOTIFY_CLIENT_SECRET`. Viktig å ikke bruke fnutter(" eller ') rundt verdiene
6. I routes.py finnes det flere metoder som via fetch_web_app kaller på Spotify sine Rest endepunkter. I metoden get_playlist_tracks mangler vi å spesifisere metoden for rest kallet. Sjekk ut dokumentasjonen til Spotify, og legg til rett metode.

### 1.1 Fiks metodene som kaller på spotify endepunkter

_I routes.py er det tre metoder som er ufullstendig implementert. Fiks metodene slik at vi kaller endepunkter i Spotify API'et på en korrekt måte._


### 1.2 Opprett en route i Frontend for å vise hjemsiden

_Den ferdiglagde komponenten PlaylistPage viser en side i frontenden der brukerne kan se alle spillelistene sine. Vi skal nå sette opp en route som viser denne som hjemmesiden_

**Oppgave**

1. Naviger til `App.tsx`, som ligger i `src`-mappen.
2. Legg til en ny route med en tom path ("/") slik at PlaylistPage blir hovedsiden.
3. Husk å importere PlaylistPage.

Når du har fullført oppgaven, skal **ImageUploadPage** vises på skjermen.

### 1.3 Legg til knapp

_PlaylistCard-komponenten er hvert kort som viser alle spillelistene til brukeren, her ønsker vi å legge til en knapp som lar brukeren komme til en ny side, med mer info om spillelisten sin, og mulighet genere coverbilde eller beskrivelse av spillelisten sin._

**Oppgave**

1. Naviger til `components/PlaylistCard/PlaylistCard.tsx`
2. Importer `Link` fra `react-router-dom`
3. Legg til en `<Link>` komponent som navigerer til `/cover/${playlist.id}`
   - Inne i Link-komponenten, legg til en `<button>` med teksten "Info"

_Hint: Link-komponenten bruker `to`-attributtet for å spesifisere hvor den skal navigere. Bruk template literals (backticks) for å inkludere playlist.id i path._

Når oppgaven er fullført, skal man kunne trykke inn på hver spilleliste, og få listet opp sanger i spillelisten. 

### 1.4 Endre bakgrunnsfarge

1. Naviger til ` cd styles/index.css `
2. Bakgrunnen er nå hvit – bytt den til din favorittfarge!


### 1.5 Lag en knapp for å generere coverbilde

_På GeneratorPage-siden vises alle sangene i spillelisten. Nå skal vi legge til en knapp som lar brukeren generere et AI-basert coverbilde for spillelisten._

**Oppgave**

1. Naviger til `pages/GeneratorPage/GeneratorPage.tsx`
2. Finn kommentaren `{/* TODO  1.5 */}` 
3. Erstatt kommentaren med en `<button>` som har følgende:
   - `onClick` skal kalle funksjonen `generateCover`
   - `disabled` skal være `true` når `generating` er `true` eller `tracks.length === 0`
   - `className` skal være `{styles.generateButton}`
   - Knappeteksten skal vise "Generating..." når `generating` er `true`, ellers "Generate AI Cover Image"

_Hint: Bruk en ternary operator (betingelse ? true : false) for å vise forskjellig tekst basert på `generating`-tilstanden._

_Hint2: Du kan se et lignende eksempel ved den andre knappen som genererer en beskrivelse av spillelisten. _

OBS: Denne knappen fungerer først fullføringen av neste oppgave.

## Oppgave 2 – INNHOLDSGENERERING  🧠

_I oppgave 2 skal bildet genereres basert på sangene i spillelisten._

---


### 2.1 BILDEGENERERING 🖼️ 

Klassen `CoverImageGeneratorClient` er laget for å samhandle med OpenAI’s gpt-image-1 gjennom Azure AI Foundry, 
og brukes til å generere bilder basert på tekstbeskrivelser (kalt "prompt").

**Oppgave**

1. Naviger til `/clients/cover_image_generator_client.py` i backend.

2. Fullfør payload med de nødvendige parameterne:
   - `prompt`: skal inneholde prompt-teksten som blir sendt inn
   - `model`: modellen vi skal bruke finner du i .env

3. Fullfør API-kallet:
   - `url`: skal peke til `self.endpoint`
   - `json`: skal inneholde `payload`
4. 

Når du har fullført oppgaven, skal det være mulig å klikke på knappen fra forrige oppgave og generere et AI-coverbilde basert på sangene i spillelisten.

### 2.2 TEKSTGENERERING 💬

Klassen `PlaylistDescriptionGeneratorClient` bruker OpenAI sin GPT-5-modell via Azure for å generere tekst basert på en prompt.
**Oppgave**

1. Naviger til `PlaylistDescriptionGeneratorClient` i backend.

2. Sett modellen til **"gpt-5"** (hentet fra .env `AZURE_OPENAI_CHAT_ENDPOINT`).


### 2.3 Forbedre Prompten 💡

_En godt formulert prompt er avgjørende for å generere relevante og presise resultater._

#### Oppgave

1. Gå gjennom eksisterende tekst i prompten i `playlist_generator.py`.

2. Sørg for at prompten er klar, spesifikk og inkluderer all nødvendig kontekst for å generere en oppskrift av høy
   kvalitet.

### 2.4 Lagre Coverbilde til Blob Storage ☁️

_Når vi har generert et coverbilde med DALL-E 3, må vi lagre det i Azure Blob Storage for permanent lagring._

**Oppgave**

1. Naviger til `clients/blob_storage_client.py` i backend.

2. I metoden `upload_image_from_url`, finn kommentaren `# TODO 2.4 Lag et unikt navn for blobben...`
   - Lag et unikt navn som følger mønsteret `covers/{user_id}/{playlist_id}.png`
   - Husk å bruke variablene `user_id` og `playlist_id` som blir sendt inn

3. Fullfør også kallet til `upload_image_from_url` i `routes.py` (linje 60) ved å kalle `get_playlist_tracks(playlist_id)` for å hente sangene fra spillelisten.

Når du har fullført oppgaven, skal coverimagene bli lagret permanent i Azure Blob Storage.

### 2.5 Liste Cover Images 📸

_Vi må kunne hente alle lagrede coverimagene for en bruker fra Blob Storage._

**Oppgave**

1. Naviger til `clients/blob_storage_client.py` i backend.

2. I metoden `list_user_covers`, finn kommentaren `# TODO 2.5 Hent ut alle blobs...`
   - Bruk `self.container_client.list_blobs(name_starts_with=prefix)` for å hente alle blobs som starter med brukerens prefix
   - Tilordne resultatet til `blob_list`

Når du har fullført oppgaven, skal du kunne se alle genererte coverimagene for en bruker på `CoverImageListPage`.

### 2.6 TEKSTGENERERING FOR BESKRIVELSE 💬

_Når vi har sangene fra spillelisten, skal vi generere en beskrivelse ved hjelp av GPT._

**Oppgave**

1. Naviger til `services/routes.py` i backend, og finn `generate_description_for_playlist`-metoden.

2. Finn kommentaren `# TODO 2.6 Kall metoden for å generere beskrivelse...`
   - Kall `description_generator.generate_description(track_names)` og tilordne resultatet til `description`-variabelen

Når du har fullført oppgaven, skal du kunne generere en AI-basert tekstbeskrivelse av spillelisten.

### 2.7 Lagre Beskrivelse til Table Storage 💾

_Etter at vi har generert en beskrivelse, skal vi lagre den permanent i Azure Table Storage for senere bruk._

**Oppgave**

1. Naviger til `services/routes.py` i backend, og finn `generate_description_for_playlist`-metoden.

2. Finn kommentaren `# TODO 2.7 Lagre den genererte beskrivelsen i table storage...`
   - Kall `table_storage.save_description_record()` med de relevante parameterne

Når du har fullført oppgaven, skal alle genererte beskrivelser bli lagret permanent i Azure Table Storage.

### 2.8 Hent Top Tracks fra Spotify API 🎵

_Nå skal vi hente brukerens mest lyttede sanger fra Spotify._

**Oppgave**

1. Naviger til `services/routes.py` i backend, og finn funksjonen `get_top_tracks`.

2. Implementer metoden slik at den henter brukerens top tracks fra Spotify Web API.
   - Hint: Se på hvordan `get_top_artists()` er implementert og gjør det samme for tracks.
   - Dokumentasjon: https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks

Når du har fullført oppgaven, skal du kunne trykke på "Tracks"-knappen på Top-siden og se dine mest lyttede sanger.

### 2.9 Sett nytt bilde for spillelisten med Spotify API 🖼️

_Vi har generert et bilde og lagret det i Blob Storage. Nå skal vi sende det til Spotify og bruke det som cover for spillelisten._

**Oppgave**

1. Naviger til `services/routes.py` i backend, og finn `set_cover_image_for_playlist`-metoden.

2. Finn kommentaren `# TODO 2.9` og erstatt placeholder-linjen med et faktisk API-kall:
   - Bruk `requests.put()` for å sende en PUT-request til Spotify
   - Riktig endpoint er `https://api.spotify.com/v1/playlists/{playlist_id}/images`
   - Body skal være `jpeg_b64` (base64-kodet JPEG)
   - Husk å sette `Content-Type: image/jpeg` og `Authorization: Bearer {token}` i headerne
   - Dokumentasjon: https://developer.spotify.com/documentation/web-api/reference/upload-custom-playlist-cover

Når du har fullført oppgaven, skal "Set as Spotify Cover"-knappen på GeneratorPage oppdatere coveret på spillelisten din direkte i Spotify.


