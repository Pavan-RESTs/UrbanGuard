const express = require("express");
const router = express.Router();
const { sendEmailToResidents, sendEmailToAuthorities } = require("../controllers/mailController");

router.post("/send-resident-alert", sendEmailToResidents);
router.post("/send-authority-alert", sendEmailToAuthorities);

module.exports = router;
