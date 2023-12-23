const bad_words = require("./Profanity.json");


/**
 * Filters out profanity from the input text based on a predefined list of bad words and their replacements.
 * @param {string} inputText - The text to be filtered for profanity.
 * @returns {string} The cleaned text with profanity replaced by safe alternatives.
 */
module.exports.FilterBadWords = function FilterBadWords(inputText) {
    let cleanedWord = inputText.toLowerCase();

    // Iterate through the list of bad words
    bad_words.forEach((entry) => {
        // Create a regular expression with the bad word
        const regex = new RegExp(escapeRegExp(entry.word), 'gi');

        // Replace profanity while preserving non-profane parts of the word
        cleanedWord = cleanedWord.replace(regex, entry.replacement);
    });

    return cleanedWord;
};

// Function to escape special characters in a string for regex
function escapeRegExp(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}