import { Route, Routes } from "react-router-dom";
import Sidebar from "./components/common/Sidebar";

import OverviewPage from "./pages/OverviewPage";
import AlertsPage from "./pages/AlertsPage";
import UsersPage from "./pages/UsersPage";
import SettingsPage from "./pages/SettingsPage";
import NearestCCTVs from "./pages/NearestCCTVs";
import NotifyPage from "./pages/NotifyPage";

function App() {
  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 overflow-hidden">

      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/case-statistics" element={<UsersPage />} />

          <Route path="/notify" element={<NotifyPage />} />


          <Route path="/settings" element={<SettingsPage />} />

          <Route path="/nearest-cctvs" element={<NearestCCTVs />} />
          
        </Routes>
      </div>
    </div>
  );
}

export default App;
