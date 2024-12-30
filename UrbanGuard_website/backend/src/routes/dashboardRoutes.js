// routes/dashboardRoutes.js
const express = require('express');
const { getDashboardStats } = require('../controllers/dashboardController');

const router = express.Router();

// Route to fetch and store statistics
router.get('/fetch-stats', getDashboardStats);

module.exports = router;
