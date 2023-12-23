const sql = require("mssql");
const app_config = require("../Configuration.json");
const { decrypt } = require("../encryption");
const { FilterBadWords } = require('../ProfanityFilter')

const config = {
  user: app_config.ConnectionSettings.username,
  password: app_config.ConnectionSettings.password,
  server: app_config.ConnectionSettings.server,
  database: app_config.ConnectionSettings.database,
  options: {
    encrypt: true,
  },
};

module.exports = async function (context, req) {
  try {
    let auth_response = AuthenticateRequest(req);

    if (!auth_response.authenticated) throw new Error(auth_response.error);

    let playerName = req.body.playerName;
    let playerScore = req.body.playerScore;
    let difficulty = req.body.playerDifficulty
    // Get the client's IP address from the headers
    let host = req.headers["host"] ?? 'N/A'
    let ip = (req.headers["x-forwarded-for"] || req.headers["x-client-ip"] || req.ip) ?? '?';

    let response = await SubmitPlayerScore(FilterBadWords(playerName), playerScore, difficulty, host, ip);
    context.res = {
      status: 200,
      body: response,
    };
  } catch (error) {
    context.res = {
      status: 500,
      body: { success: false, error: error.toString() },
    };
  }
};

/**
 * Authenticates incoming requests by validating the secret key
 * @param {httpIncomingMessage} req  - the incoming http request
 * @returns {object}  an object containing the authentication result
 */
function AuthenticateRequest(req) {
  try {
    let secretKey = req.headers["x-secretkey"];
    // Check if X-SecretKey header is present
    if (!secretKey) {
      return { authenticated: false, error: "X-SecretKey header is missing" };
    } else {
      //decrypt here
      secretKey = decrypt(Buffer.from(secretKey, "hex"), Buffer.from(app_config.SecretKey, "hex"));
      if (secretKey === app_config.ServerSecret) return { authenticated: true };
      else return { authenticated: false, error: "invalid secret" };
    }
  } catch (error) {
    return { authenticated: false, error: error.toString() };
  }
}

/**
 * Initializes the sql connection, returns the connection if already established
 * @returns {SqlConnection} the connection object
 */
function GetConnection() {
  return new Promise(async (resolve) => {
    sql
      .connect(config)
      .then((connection) => {
        return resolve(connection);
      })
      .catch((error) => {
        console.log("connection failed :" + error);
        return resolve(null);
      });
  });
}

/**
 * Submit player score to the database
 * @param {string} playerName - The name of the player
 * @param {number} playerScore - The score achieved by the player
 * @param {string} host - The host of the incoming request
 * @param {string} ip - The IP address of the player
 * @returns {Promise} A promise that resolves with the result of the database operation
 */
function SubmitPlayerScore(playerName, playerScore, difficulty, host, ip) {
  return new Promise(async (resolve) => {
    try {
      let connection = await GetConnection();
      if (!connection) return resolve({ success: false, error: "could not connect to the database" });

      // Update the SQL query to use named parameters
      const query = `
          INSERT INTO PlayerScores (name, score, difficulty, host, ip, timestamp)
          VALUES (@playerName, @playerScore, @difficulty, @host, @ip, @timestamp)
        `;

      const request = connection.request();
      request.input("playerName", sql.VarChar(255), playerName); // Adjust the length based on your database schema
      request.input("playerScore", sql.Int, playerScore);
      request.input("difficulty", sql.VarChar(15), difficulty);
      request.input("host", sql.VarChar(255), host);
      request.input("ip", sql.VarChar(255), ip); // Adjust the length based on your database schema
      request.input("timestamp", sql.DateTime, new Date());

      request
        .query(query)
        .then((result) => {
          return resolve({ success: true, inserted: result.rowsAffected[0] });
        })
        .catch((error) => {
          return resolve({ success: false, error: error.message });
        });
    } catch (error) {
      return resolve({ success: false, error: error.toString() });
    }
  });
}
