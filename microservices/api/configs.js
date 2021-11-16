module.exports = {
	"debug": false,
	"port": process.env.PORT || 8080,
	"sql": {
		"host": process.env.DB_HOST || 'localhost',
		"database": process.env.DB_NAME || 'stond',
		"username": process.env.DB_USERNAME || 'root',
		"password": process.env.DB_PSW || 'rootroot',
		"port": process.env.DB_PORT || 3306,
		"connection_name": process.env.DB_CONN_NAME || null
	},
	"jwt": {
		'secret': 'C1v8GloASpgkfcDJd0bKLmFTvDVRyVp1'
	},
	"twilio": {
		"phoneNumber": "+447411266421",
		"accoundSID": "AC789c446a4326d347eac448421fb0665c",
		"authToken": "76a95164db067ecdd3ff10e59eb903e0"
	}
}