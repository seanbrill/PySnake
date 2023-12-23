const crypto = require("crypto");
const fs = require("fs");
const config = require("./Configuration.json");

/**
 * Encrypts a plaintext string using the provided secret key with AES-256-CBC encryption.
 * Automatically generates a random initialization vector (IV) for added security.
 * @param {string} plaintext - The string to be encrypted.
 * @param {Buffer} secretKey - The secret key used for encryption.
 * @returns {Buffer} A buffer representing the encrypted data, including the IV.
 */
module.exports.encrypt = function encrypt(plaintext, secretKey) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv("aes-256-cbc", Buffer.from(secretKey), iv);

  let encryptedData = cipher.update(plaintext, "utf-8", "hex");
  encryptedData += cipher.final("hex");

  return Buffer.concat([iv, Buffer.from(encryptedData, "hex")]);
};

/**
 * Decrypts encrypted data using the provided secret key with AES-256-CBC decryption.
 * Expects the encrypted data to include the initialization vector (IV) for proper decryption.
 * @param {Buffer} encryptedData - The encrypted data, including the IV.
 * @param {Buffer} secretKey - The secret key used for decryption.
 * @returns {string} The decrypted plaintext string.
 * @throws {Error} Throws an error if decryption fails.
 */
module.exports.decrypt = function decrypt(encryptedData, secretKey) {
  try {
    const iv = encryptedData.slice(0, 16);
    const ciphertext = encryptedData.slice(16);

    const decipher = crypto.createDecipheriv("aes-256-cbc", Buffer.from(secretKey), iv);

    let decryptedText = decipher.update(ciphertext, "hex", "utf-8");
    decryptedText += decipher.final("utf-8");

    return decryptedText;
  } catch (error) {
    console.error("Decryption error:", error.message);
    throw error;
  }
};
