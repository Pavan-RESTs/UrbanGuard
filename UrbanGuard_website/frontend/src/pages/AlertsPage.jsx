import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { FiMapPin, FiCamera, FiBell, FiTrash2, FiX, FiAlertCircle } from "react-icons/fi";
import Header from "../components/common/Header";
import { useNavigate } from "react-router-dom";  

const AlertsPage = () => {
  const [alerts, setAlerts] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [showMap, setShowMap] = useState(false);   
  const [showFootage, setShowFootage] = useState(true);   

  const navigate = useNavigate(); 
  const fetchAlerts = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/alerts/fetch-alerts");
      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      console.error("Error fetching alerts:", error);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const handleLocateAnomaly = (coordinates) => {
    const { lat, lng } = coordinates;
    const googleMapsUrl = `https://www.google.com/maps?q=${lat},${lng}&z=15&output=embed`;
    setSelectedAlert((prev) => ({
      ...prev,
      googleMapsUrl: googleMapsUrl
    }));
    setShowMap(true);  // Set to show the map
  };

  const handleViewNearestCCTV = (coordinates, locality) => {
    console.log("Co-ordinates:", coordinates, "Locality: ", locality);
    navigate("/nearest-cctvs", {
      state: { coordinates: coordinates, locality: locality },
    });
  };

  const handleNotify = () => {
    alert("Notification sent successfully!");
  };

  const handleDeleteAlert = async (id) => {
    try {
      const response = await fetch(`http://localhost:5000/api/alerts/delete-alerts/${id}`, {
        method: "DELETE",
      });
      if (response.ok) {
        setAlerts((prevAlerts) => prevAlerts.filter((alert) => alert._id !== id));
        alert("Alert deleted successfully");
        window.location.reload();
        setShowPopup(false);
      } else {
        alert("Failed to delete alert");
      }
    } catch (error) {
      console.error("Error deleting alert:", error);
    }
  };

  const handlePopupOpen = (alert) => {
    setSelectedAlert(alert);
    setShowPopup(true);
  };

  const handlePopupClose = () => {
    setShowPopup(false);
    setSelectedAlert(null);
    setShowMap(false); // Reset map view
    setShowFootage(false); // Reset footage view
  };

  return (
    <div className="flex-1 overflow-auto relative z-10 bg-gray-900 text-gray-100">
      <Header title="Alerts" />

      <main className="max-w-7xl mx-auto py-6 px-4 lg:px-8">
        {alerts.length === 0 ? (
          <p>No alerts available.</p>
        ) : (
          <div className="space-y-4">
            {alerts.map((alert) => (
              <div
                key={alert._id}
                className="bg-red-700 p-4 rounded-lg shadow-md hover:bg-red-600 hover:scale-105 transition-all transform cursor-pointer relative"
                onClick={() => handlePopupOpen(alert)}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-transparent opacity-30 blur-md rounded-lg"></div>
                <div className="relative z-10 flex items-center justify-center space-x-2">
                  <FiAlertCircle size={24} className="text-white" />
                  <h3 className="text-lg text-white font-semibold text-center">
                    Alert Received at {alert.anomalyTime}! Click here to get more info!
                  </h3>
                </div>
              </div>
            ))}
          </div>
        )}

        {showPopup && selectedAlert && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <motion.div
              className="relative bg-gradient-to-br from-gray-600 via-white-100 to-white-600 rounded-lg shadow-lg p-6 text-white"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ duration: 0.3 }}
              style={{ width: "90%", maxWidth: "800px" }}
            >
              <button
                className="absolute top-3 right-3 text-white hover:text-gray-300"
                onClick={handlePopupClose}
              >
                <FiX size={24} />
              </button>

              <h2 className="text-2xl font-bold mb-4 text-center">Alert Details</h2>

              {/* Conditional Rendering for Map or Video */}
              {showMap ? (
                <div className="relative w-full mb-6" style={{ paddingBottom: "75%" }}>
                  <iframe
                    src={selectedAlert.googleMapsUrl}
                    width="100%"
                    height="100%"
                    style={{
                      zIndex: 3,
                      position: "absolute",
                      height: "100%",
                      width: "100%",
                      padding: "0px",
                      borderWidth: "0px",
                      margin: "0px",
                      left: "0px",
                      top: "0px",
                      touchAction: "pan-x pan-y",
                    }}
                    allowFullScreen=""
                    loading="lazy"
                  ></iframe>
                  <button
                    className="absolute top-3 right-3 text-white bg-black bg-opacity-50 rounded-full p-2"
                    onClick={() => setShowMap(false)}  
                  >
                    <FiX size={24} />
                  </button>
                </div>
              ) : showFootage ? (
                <div className="relative w-full mb-6" style={{ paddingBottom: "56.25%" }}>
                  <video
                    className="absolute top-0 left-0 w-full h-full rounded-lg shadow-lg"
                    src={selectedAlert.footageUrl}
                    controls
                    autoPlay
                    muted
                  >
                    Your browser does not support the video tag.
                  </video>
                </div>
              ) : (
                <div className="mt-6 w-full h-[400px]">
                
                </div>
              )}
              <div className="grid grid-cols-2 gap-4 mt-4">
  <button
    className="flex items-center justify-center bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md shadow-lg transition duration-300"
    onClick={() => handleLocateAnomaly(selectedAlert.coordinates)}
  >
    <FiMapPin size={20} className="mr-2" /> Locate Anomaly
  </button>

  <button
    className="flex items-center justify-center bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-md shadow-lg transition duration-300"
    onClick={() => handleViewNearestCCTV(selectedAlert.coordinates, selectedAlert.location)}
  >
    <FiCamera size={20} className="mr-2" /> View Nearest CCTV
  </button>

  <button
    className="flex items-center justify-center bg-yellow-500 hover:bg-yellow-600 text-white py-2 px-4 rounded-md shadow-lg transition duration-300"
    onClick={handleNotify}
  >
    <FiBell size={20} className="mr-2" /> Notify
  </button>

  <button
    className="flex items-center justify-center bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-md shadow-lg transition duration-300"
    onClick={() => handleDeleteAlert(selectedAlert._id)}
  >
    <FiTrash2 size={20} className="mr-2" /> Delete Alert
  </button>
</div>

{/* New "View Footage" button */}
<div className="flex justify-center mt-4">
  <button
    className="flex items-center justify-center bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md shadow-lg transition duration-300"
    onClick={() => {
      setShowMap(false);   
      setShowFootage(true);  
    }}
  >
    View Footage
  </button>
</div>

            </motion.div>
          </div>
        )}
      </main>
    </div>
  );
};

export default AlertsPage;
