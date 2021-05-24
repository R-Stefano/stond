const path = require('path')
const axios = require('axios')
configs = require('../configs.js')

if (process.argv.includes("production")) {
} else if (process.argv.includes("staging")) {
    configs.sql.host = "35.189.121.159"
    configs.sql.database = ""
    configs.sql.username = "root"
    configs.sql.password = "root"
    configs.cloud.bucket_name = ""
} else {
    console.log("Syncing Local DB")
}

const db = require('../libs/db')
const { Op } = require("sequelize");

/*
const {Storage} = require('@google-cloud/storage');
const storage = new Storage({keyFilename: path.resolve(__dirname, '../../' + configs.cloud.bucket_auths)});
const GCBucket = storage.bucket(configs.cloud.bucket_name);
*/



db.sequelize.sync({force: true})
.then(() => {
    createResourcesPermissionsRoles()
    createUsers()
    initializeStore()
    console.log("<<DONE>>")
})
.catch((e) => {
    console.log(e)
})

async function createResourcesPermissionsRoles() {
    //const resources = await Promise.all([
    //    db.resource.findOrCreate({defaults: {}, where: {}})
    //])

    //const permissions = await Promise.all([
    //    db.permission.findOrCreate({defaults: {}, where: {}})
    //])

    const roles = await Promise.all([
        db.role.findOrCreate({defaults: {name: 'shop manager', notes: '', companyBranchID: null, type: 'shop_manager'}, where: {name: 'shop manager'}}),
        db.role.findOrCreate({defaults: {name: 'consignor',    notes: '', companyBranchID: null, type: 'consignor'}, where: {name: 'consignor'}}),
        db.role.findOrCreate({defaults: {name: 'editmanldn',   notes: '', companyBranchID: 1, type: 'company'}, where: {name: 'shop manager'}})
    ])
}

async function createUsers() {
    const userShop = await db.user.create({
        companyBranchID: 1,
        email: 'millie@theeditmanlondon.com',
        name: 'camilla',
        surname: 'Pearson',
        password: 'millie',
        activatedAt: new Date()
    })

    const userConsignor = await db.user.create({
        companyBranchID: 1,
        email: 'consignor@test.com',
        name: 'consignor',
        surname: 'consignor',
        password: 'consignor',
        activatedAt: new Date()
    })

    const editmanldnRole = await db.role.findOne({where: {name: 'editmanldn'}})
    const shopManagerRole = await db.role.findOne({where: {name: 'shop manager'}})
    const consignorRole = await db.role.findOne({where: {name: 'consignor'}})

    await Promise.all([
        db.user_role.findOrCreate({defaults: {roleID: editmanldnRole.ID, userID: userShop.ID}, where: {roleID: editmanldnRole.ID, userID: userShop.ID}}),
        db.user_role.findOrCreate({defaults: {roleID: shopManagerRole.ID, userID: userShop.ID}, where: {roleID: shopManagerRole.ID, userID: userShop.ID}})
    ])

    await Promise.all([
        db.user_role.findOrCreate({defaults: {roleID: editmanldnRole.ID, userID: userConsignor.ID}, where: {roleID: editmanldnRole.ID, userID: userConsignor.ID}}),
        db.user_role.findOrCreate({defaults: {roleID: consignorRole.ID, userID: userConsignor.ID}, where: {roleID: consignorRole.ID, userID: userConsignor.ID}})
    ])
}

async function initializeStore() {
    /**
     * Download all products
     * 
     * - PRODUCT CATEGORIES
     *      - extract unique categories & import them
     * - PRODUCTS 
     *      - extract unique products (should be all of them) & import them
     * - PRODUCS VARIANTS 
     *      - extract products variants, match them with the product & import them
     * - PRODUCTS IMAGES
     *      - 
     * - ITEMS
     *      
     */
    const clientID = 1
    const fs = require('fs')

    let shopifyProducts = await axios.get(`https://${configs.shopify.username}:${configs.shopify.password}@${configs.shopify.shop}.myshopify.com/admin/api/2021-04/products.json`) //JSON.parse(fs.readFileSync('./tests/data/shopify/api_products.json', 'utf-8')).products
    shopifyProducts = shopifyProducts.data.products

    console.log(`>> Importing Products Categories`)
    const _extractedProductsCategories = shopifyProducts.map(shopifyProduct => shopifyProduct.product_type.trim().toLowerCase())
    /**
     * TODO:
     *  1. Merge similar categories
     *      - sneaker:sneakers -> sneaker
     *      - t shirts;t-shirt;t shirt -> t shirt
     *  2. Consider that there is VARIOUS product & Category for each client
     */
    const uniqueProductCategories = [... new Set(_extractedProductsCategories)] 
    let productCategories = await Promise.all(uniqueProductCategories.map(productCategoryName => db.productCategory.findOrCreate({where: {clientID: clientID, name: productCategoryName}, defaults: {clientID: clientID, name: productCategoryName}})))
    productCategories = productCategories.map(results => results[0])
    console.log(`Product Categories Extracted: ${uniqueProductCategories.length} | Imported: ${productCategories.length}`)

    console.log(`>> Importing Products`)
    const shopifyProductsVariants = []
    const products = shopifyProducts.map(shopifyProduct => {
        const category = productCategories.find(productCategory => productCategory.name == shopifyProduct.product_type.trim().toLowerCase())
        shopifyProductsVariants.push(...shopifyProduct.variants)

        return {
            foreignID: shopifyProduct.id, 
            clientID: clientID,
            code: shopifyProduct.title.trim().toLowerCase(),
            description: shopifyProduct.vendor.trim().toLowerCase(),
            weight: shopifyProduct.variants[0].weight,
            pieces: 1,
            categoryID: category.ID
        }
    })
    console.log(`Products Extracted: ${products.length} | Ready to Import: ${[... new Set(products.map(product => product.foreignID))].length}`)
    const importedProducts = await db.product.bulkCreate(products, {updateOnDuplicate: ['foreignID']})

    console.log(`Products Variants Extracted: ${shopifyProductsVariants.length}`)
    const productsVariants = shopifyProductsVariants.map(productVariant => {
        const _prod = importedProducts.find(product => product.foreignID == productVariant.product_id)

        const options = []
        productVariant.option1 ? options.push(productVariant.option1) : null
        productVariant.option2 ? options.push(productVariant.option2) : null
        productVariant.option3 ? options.push(productVariant.option3) : null
        return {
            foreignID: productVariant.id,
            productID: _prod.ID,
            name: productVariant.title,
            price: productVariant.price,
            options: `${options.reduce((text, option, idx) => text += `${idx > 0 ? ':' : ''}${option}`, '')}`,
            weight: productVariant.weight,
            volume: 0
        }
    })

    const importedProductsVariants = await Promise.all(productsVariants.map(productVariant => db.productVariant.findOrCreate({defaults: productVariant, where: {productID: productVariant.productID, name: productVariant.name}})))
    console.log(`Products Variants Imported: ${importedProductsVariants.length}`)

    console.log(`>> Importing Products Images`)
    const shopifyProductsImages = []
    shopifyProducts.map(shopifyProduct => shopifyProductsImages.push(...shopifyProduct.images))
    console.log(`Products Images Extracted: ${shopifyProductsImages.length}`)
    const productsImages =  shopifyProductsImages.map(shopifyProductsImage => {
        const _prod = importedProducts.find(product => product.foreignID == shopifyProductsImage.product_id)
        return {
            productID: _prod.ID,
            filename: null,
            src: shopifyProductsImage.src
        }
    })
    const importedProductsImages = await Promise.all(productsImages.map(productImage => db.productImage.findOrCreate({defaults: productImage, where: {productID: productImage.productID}})))
    console.log(`Products Images Imported: ${importedProductsImages.length}`)
}