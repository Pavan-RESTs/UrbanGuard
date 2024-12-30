const { sendEmail } = require("../services/emailService");
const Resident = require("../models/Resident");
const Authority = require("../models/Authority");

const sendEmailToResidents = async (req, res) => {
  try {
    const residents = await Resident.find();
    const subject = "Alert: Important Notification";
    const text = "This is an important alert message sent to all residents.";

    for (const resident of residents) {
      await sendEmail(resident.email, subject, text);
    }

    res.status(200).json({ message: "Emails sent successfully to all residents." });
  } catch (error) {
    res.status(500).json({ message: "Failed to send emails", error });
  }
};

const sendEmailToAuthorities = async (req, res) => {
  try {
    const authorities = await Authority.find();
    const subject = "Alert: Important Notification";
    const text = "This is an important alert message sent to all authorities.";

    for (const authority of authorities) {
      await sendEmail(authority.email, subject, text);
    }

    res.status(200).json({ message: "Emails sent successfully to all authorities." });
  } catch (error) {
    res.status(500).json({ message: "Failed to send emails", error });
  }
};

module.exports = { sendEmailToResidents, sendEmailToAuthorities };
