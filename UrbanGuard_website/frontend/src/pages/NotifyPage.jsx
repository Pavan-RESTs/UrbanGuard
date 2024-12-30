import React, { useState, useEffect } from "react";
import { FaUserPlus, FaEnvelope, FaUserShield } from "react-icons/fa";
import { IoPeople, IoShieldCheckmark } from "react-icons/io5";
import axios from "axios";
import Header from "../components/common/Header";

const AddUserModal = ({ userType, setShowModal }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [locality, setLocality] = useState("");

  const handleSubmit = async () => {
    try {
      const user = { name, email, locality };
      const endpoint =
        userType === "resident" ? "/api/residents/add-resident" : "/api/authorities/add-authority";

      const response = await axios.post(`http://localhost:5000${endpoint}`, user);
      if (response.status === 200) {
        alert(`${userType === "resident" ? "Resident" : "Authority"} added successfully!`);
        setShowModal(false);
      }
    } catch (error) {
      console.error(error);
      alert("Failed to add user.");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 text-white rounded-lg p-6 w-96">
        <h3 className="text-xl mb-4">
          Add {userType === "resident" ? "Resident" : "Authority"} User
        </h3>
        <div className="mb-4">
          <label className="block mb-1">Name</label>
          <input
            type="text"
            className="w-full p-2 border border-gray-600 rounded bg-gray-700 text-white"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Email</label>
          <input
            type="email"
            className="w-full p-2 border border-gray-600 rounded bg-gray-700 text-white"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Locality</label>
          <input
            type="text"
            className="w-full p-2 border border-gray-600 rounded bg-gray-700 text-white"
            value={locality}
            onChange={(e) => setLocality(e.target.value)}
          />
        </div>
        <div className="flex justify-end gap-4">
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
            onClick={handleSubmit}
          >
            Add
          </button>
          <button
            className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
            onClick={() => setShowModal(false)}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

const UserTable = ({ users, userType }) => (
  <div className="space-y-6">
    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
      {userType === "resident" ? <IoPeople /> : <IoShieldCheckmark />}
      {userType === "resident" ? "Resident Users" : "Authority Users"}
    </h3>
    <table className="w-full text-left border border-gray-300">
      <thead>
        <tr>
          <th className="border border-gray-300 p-2">Name</th>
          <th className="border border-gray-300 p-2">Email</th>
          <th className="border border-gray-300 p-2">Locality</th>
        </tr>
      </thead>
      <tbody>
        {users.map((user) => (
          <tr key={user.email}>
            <td className="border border-gray-300 p-2">{user.name}</td>
            <td className="border border-gray-300 p-2">{user.email}</td>
            <td className="border border-gray-300 p-2">{user.locality}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);


const NotifyPage = () => {
  const [showAddUserModal, setShowAddUserModal] = useState(false);
  const [userType, setUserType] = useState("");
  const [residentUsers, setResidentUsers] = useState([]);
  const [authorityUsers, setAuthorityUsers] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/residents/get-residents")
      .then((response) => setResidentUsers(response.data))
      .catch((error) => console.error(error));

    axios
      .get("http://localhost:5000/api/authorities/get-authorities")
      .then((response) => setAuthorityUsers(response.data))
      .catch((error) => console.error(error));
  }, []);

  const handleAddUserClick = (type) => {
    setUserType(type);
    setShowAddUserModal(true);
  };

  const handleSendEmail = (type) => {
    const endpoint =
      type === "resident" ? "/api/mail/send-resident-alert" : "/api/mail/send-authority-alert";

    axios
      .post(`http://localhost:5000${endpoint}`)
      .then((response) => alert(response.data.message))
      .catch(() => alert(`Failed to send email to ${type}s.`));
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-64 bg-gray-800 text-white p-4 space-y-4">
        <h2 className="text-xl font-bold">Urban Guard</h2>
        <button
          className="w-full p-3 bg-blue-600 hover:bg-blue-700 rounded flex items-center gap-2"
          onClick={() => handleAddUserClick("resident")}
        >
          <FaUserPlus /> Add Resident User
        </button>
        <button
          className="w-full p-3 bg-green-600 hover:bg-green-700 rounded flex items-center gap-2"
          onClick={() => handleAddUserClick("authority")}
        >
          <FaUserShield /> Add Authority User
        </button>
      </div>
      <div className="flex-1 bg-gray-900 p-8 space-y-8">
        <Header title="Notify Service" />
        <div>
          <UserTable users={residentUsers} userType="resident" />
          <div className="flex justify-center mt-4">
            <button
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded flex items-center gap-2"
              onClick={() => handleSendEmail("resident")}
            >
              <FaEnvelope /> Notify Residents
            </button>
          </div>
        </div>
        <div>
          <UserTable users={authorityUsers} userType="authority" />
          <div className="flex justify-center mt-4">
            <button
              className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded flex items-center gap-2"
              onClick={() => handleSendEmail("authority")}
            >
              <FaEnvelope /> Notify Authorities
            </button>
          </div>
        </div>
      </div>
      {showAddUserModal && <AddUserModal userType={userType} setShowModal={setShowAddUserModal} />}
    </div>
  );
};

export default NotifyPage;
