module.exports = {
	"debug": false,
	"port": process.env.PORT || 8080,
	"sql": {
		"host": process.env.DB_HOST || 'localhost',
		"database": process.env.DB_NAME || 'consignor-platform',
		"username": process.env.DB_USERNAME || 'root',
		"password": process.env.DB_PSW || 'rootroot',
		"port": process.env.DB_PORT || 3306,
		"connection_name": process.env.DB_CONN_NAME || null
	},
	"jwt": {
		'secret': 'C1v8GloASpgkfcDJd0bKLmFTvDVRyVp1'
	}
}