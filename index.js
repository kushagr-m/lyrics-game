const encode64 = btoa;
const decode64 = atob;
const api_baseurl = "https://h0o0hqgvte.execute-api.ap-southeast-2.amazonaws.com/prod";

var app = new Vue({
    el: '#app',
    data: {
        loading: true,
        lyrics: '',
        input_box: '',
        columns: 8,
        found_words: [],
        game_state: 0, // 0 = playing, 1 = loss, 2 = win
    },
    computed: {
        total_count: function() {
            return this.lyrics ? this.lyrics.split(" ").length : 0;
        },
        words_per_column: function() {
            return Math.floor(this.total_count / this.columns) + 1;
        },
        raw_lyrics: function() {
            // IS AN ARRAY OF WORDS
            // raw lyrics, without quotations or punctuation
            return this.lyrics.replace(/[.,\/#!$%\^&\*\"\'\?;:{}=\-_`~()]/g,"").toLowerCase().split(' ');
        },
        lyrics_arr: function() {
            return this.lyrics.split(' ');
        },
        num_found_words: function() {
            let num = 0
            for (let word of this.raw_lyrics) {
                if (this.found_words.includes(word)) num++;
            }
            return num;
        }
    },
    watch: {
        lyrics: function(val) {
            // Normalise whitespace, restrict to ASCII characters
            this.lyrics = this.lyrics.replace(/[\u{0080}-\u{FFFF}]/gu,"").replace(/\s+/g, ' ');
        },
        input_box: function(val) {
            // Normalise -- replace lowercase, punctuation, non-ascii and excess spaces
            let word = val.toLowerCase().replace(/[.,\/#!$%\^&\*\"\'\?;:{}=\-_`~()]/g,"").replace(/[\u{0080}-\u{FFFF}]/gu,"").replace(/\s+/g, ' ');
            console.log(word);
            if (!this.found_words.includes(word) && this.raw_lyrics.includes(word)) {
                // We've found a new word!
                this.input_box = '';
                this.found_words.push(word);
            }
        }
    }
});

async function main() {
    // The path of the lyrics will be encoded base64 in the url to allow for sharing.
    const params = new URLSearchParams(window.location.search);
    const path = decode64(params.get("path"));
    const lyrics = await get_lyrics(path);
    if (lyrics) {
        app.loading = false;
        app.lyrics = lyrics;
    }
    // PoC: Green Day- american idiot http://localhost:8000/?path=L2x5cmljcy9ncmVlbmRheS9hbWVyaWNhbmlkaW90Lmh0bWw
}

async function get_lyrics(path) {
    const api_path = '/';
    let lyrics;
    await $.post( api_baseurl + api_path, { path: path }, function(response) {
        lyrics = (response)['lyrics'];
    });
    return lyrics;
}

main();
