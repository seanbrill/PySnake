const sql = require("mssql");
const app_config = require("../Configuration.json");

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
    let response = await GetLeaderboard();
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
 * Removes duplicates from an array of objects based on the "name" property,
 * keeping only the object with the highest score for each unique name.
 * @param {object[]} arr - An array of objects with "name" and "score" properties.
 * @returns {object[]} An array containing unique objects with the highest score for each unique name.
 */
function RemoveDuplicates(arr) {
  const uniqueObjectsMap = new Map();

  // Use reduce to iterate through the array
  const resultArray = arr.reduce((acc, obj) => {
    const { name, score } = obj;

    // If the name is not in the Map or the score is higher, update the Map
    if (!uniqueObjectsMap.has(name) || score > uniqueObjectsMap.get(name).score) {
      uniqueObjectsMap.set(name, obj);
    }

    return acc;
  }, []);

  // Convert the values of the Map back to an array
  return Array.from(uniqueObjectsMap.values());
}

/**
 * Gets the sorted leaderboard from the database
 * @returns {Promise<object>}  a promise containing the success result of the function call
 */
function GetLeaderboard() {
  return new Promise(async (resolve) => {
    try {
      let connection = await GetConnection();
      if (!connection) return resolve({ success: false, error: "could not connect to the database" });
      sql
        .query(`select top(100) "name", score, difficulty from PlayerScores order by score desc`)
        .then((result) => {
          return resolve({ success: true, leaderboard: RemoveDuplicates(result.recordset) });
        })
        .catch((error) => {
          return resolve({ success: false, error: error.message });
        });
    } catch (error) {
      return resolve({ success: false, error: error.toString() });
    }
  });
}
