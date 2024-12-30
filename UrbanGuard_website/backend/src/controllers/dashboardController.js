// controllers/dashboardController.js
const { fetchAndStoreDashboardData } = require('../services/dashboardService');

// Endpoint to fetch and store statistics
const getDashboardStats = async (req, res) => {
  try {
    const stats = await fetchAndStoreDashboardData();
    res.status(200).json(stats);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching dashboard statistics.' });
  }
};

module.exports = { getDashboardStats };
