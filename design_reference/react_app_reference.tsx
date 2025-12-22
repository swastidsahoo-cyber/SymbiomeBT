import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Button } from './components/ui/button';
import { Badge } from './components/ui/badge';
import { ScrollArea } from './components/ui/scroll-area';
import {
  Home,
  Activity,
  Gamepad2,
  BarChart3,
  Globe,
  Sprout,
  Bot,
  Menu,
  X,
  Sparkles,
  Heart,
  CloudSun,
  GraduationCap,
  Brain,
  BellRing,
  Rocket,
  Beaker,
  Settings,
  Target,
  FlaskConical,
  Eye,
  ChevronRight,
  Zap,
  MessageSquare,
  Trophy,
  Hand,
  Shield,
  Users,
  TrendingUp,
  Cpu,
} from 'lucide-react';

// Import all main components
import { DashboardHome } from './components/DashboardHome';
import { MonitoringSession } from './components/MonitoringSession';
import { BiofeedbackGame } from './components/BiofeedbackGame';
import { AnalysisDashboard } from './components/AnalysisDashboard';
import { CommunityCloud } from './components/CommunityCloud';
import { EnvironmentalFeedback } from './components/EnvironmentalFeedback';
import { DigitalTwin } from './components/DigitalTwin';
import { EmotionalJournal } from './components/EmotionalJournal';
import { ResilienceForecast } from './components/ResilienceForecast';
import { EducationalPortal } from './components/EducationalPortal';
import { CognitiveGames } from './components/CognitiveGames';
import { AdaptiveCoach } from './components/AdaptiveCoach';
import { FutureVision } from './components/FutureVision';
import { SimulationSandbox } from './components/SimulationSandbox';
import { SettingsPrivacy } from './components/SettingsPrivacy';
import { CustomStress } from './components/CustomStress';
import { ScientificAnalysis } from './components/ScientificAnalysis';
import { PassiveMonitoring } from './components/PassiveMonitoring';

// Import new competition-winning components
import { AdvancedPredictiveEngine } from './components/AdvancedPredictiveEngine';
import { ClosedLoopBiofeedback } from './components/ClosedLoopBiofeedback';
import { NLPJournaling } from './components/NLPJournaling';
import { ResilienceQuotient } from './components/ResilienceQuotient';
import { DigitalTwinAdvanced } from './components/DigitalTwinAdvanced';
import { GloveVisualization } from './components/GloveVisualization';
import { ClinicalDataVault } from './components/ClinicalDataVault';
import { CommunityResilienceMap } from './components/CommunityResilienceMap';
import { AdvancedFeatures } from './components/AdvancedFeatures';

import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner';

// Import types and utilities
import type { SessionData, BiometricReading, UserProfile } from './types/symbiome';
import {
  generateHistoricalSessions,
  calculateResilienceScore,
  generateAIPrediction,
  generateCommunityData,
  generateEnvironmentalData,
} from './utils/dataSimulator';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [sessions, setSessions] = useState<SessionData[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showCoach, setShowCoach] = useState(false);
  const [userProfile, setUserProfile] = useState<UserProfile>({
    name: 'Researcher',
    level: 5,
    xp: 4250,
    streak: 7,
    totalSessions: 42,
    achievements: [],
  });

  // Initialize data
  useEffect(() => {
    const historicalSessions = generateHistoricalSessions(14);
    setSessions(historicalSessions);
    toast.success('Symbiome Platform Initialized', {
      description: 'Welcome to your resilience ecosystem',
    });

    // Show coach after 5 seconds
    const timer = setTimeout(() => {
      setShowCoach(true);
    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  // Calculate current metrics
  const resilienceScore = calculateResilienceScore(sessions);
  const prediction = generateAIPrediction(resilienceScore.overall);
  const communityData = generateCommunityData();
  const environmentalData = generateEnvironmentalData();

  // Prepare weekly data for charts
  const weeklyData = Array.from({ length: 7 }, (_, i) => {
    const day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i];
    const daySessions = sessions.filter((s) => {
      const sessionDay = new Date(s.date).getDay();
      return sessionDay === (i + 1) % 7;
    });
    const avgSRI = daySessions.length > 0
      ? daySessions.reduce((sum, s) => sum + s.sri, 0) / daySessions.length
      : resilienceScore.overall;
    return { day, sri: avgSRI };
  });

  const handleCompleteSession = (readings: BiometricReading[]) => {
    if (readings.length === 0) return;

    const avgHRV = readings.reduce((sum, r) => sum + r.hrv, 0) / readings.length;
    const avgGSR = readings.reduce((sum, r) => sum + r.gsr, 0) / readings.length;
    const avgFacial = readings.reduce((sum, r) => sum + r.facialCalm, 0) / readings.length;
    
    const newSession: SessionData = {
      id: `session-${Date.now()}`,
      date: Date.now(),
      duration: readings.length,
      avgHRV,
      avgGSR,
      avgFacialCalm: avgFacial,
      sri: (avgHRV * 0.35 + (100 - avgGSR) * 0.3 + avgFacial * 0.35),
      recoveryTime: Math.floor(Math.random() * 300) + 180,
      stressEvents: Math.floor(Math.random() * 5),
      type: 'stress',
    };

    setSessions((prev) => [...prev, newSession]);
    setUserProfile((prev) => ({
      ...prev,
      xp: prev.xp + 150,
      totalSessions: prev.totalSessions + 1,
    }));

    toast.success('Session Completed!', {
      description: `SRI: ${newSession.sri.toFixed(1)} | +150 XP earned`,
    });

    setActiveTab('home');
  };

  const navigationItems = [
    { id: 'home', label: 'Dashboard', icon: Home, color: 'text-teal-400' },
    
    // Section: Real-Time Monitoring
    { id: 'monitor', label: 'Live Monitor', icon: Activity, color: 'text-green-400' },
    { id: 'passivemonitoring', label: 'Passive Sentinel', icon: Eye, color: 'text-purple-400' },
    { id: 'customstress', label: 'Custom Activities', icon: Target, color: 'text-orange-400' },
    
    // Section: Training & Intervention
    { id: 'train', label: 'Biofeedback Training', icon: Gamepad2, color: 'text-pink-400' },
    { id: 'closedloop', label: 'Closed-Loop System', icon: Zap, color: 'text-yellow-400' },
    { id: 'cognitive', label: 'Cognitive Tests', icon: Brain, color: 'text-purple-400' },
    
    // Section: AI & Prediction
    { id: 'predictive', label: 'Predictive Engine', icon: TrendingUp, color: 'text-red-400' },
    { id: 'twin', label: 'Digital Twin (Basic)', icon: Bot, color: 'text-cyan-400' },
    { id: 'twinadvanced', label: 'Digital Twin (In-Silico)', icon: Cpu, color: 'text-blue-400' },
    { id: 'forecast', label: 'Resilience Forecast', icon: CloudSun, color: 'text-blue-400' },
    
    // Section: Data & Analysis
    { id: 'journal', label: 'Emotional Journal (Basic)', icon: Heart, color: 'text-red-400' },
    { id: 'nlpjournal', label: 'NLP Sentiment AI', icon: MessageSquare, color: 'text-pink-400' },
    { id: 'rqtracker', label: 'Resilience Quotient™', icon: Trophy, color: 'text-amber-400' },
    { id: 'environment', label: 'Environment Tracker', icon: Sprout, color: 'text-green-400' },
    { id: 'scientificanalysis', label: 'Scientific Analysis', icon: FlaskConical, color: 'text-yellow-400' },
    { id: 'analysis', label: 'Research Dashboard', icon: BarChart3, color: 'text-indigo-400' },
    
    // Section: Hardware & Clinical
    { id: 'glove', label: 'Symbiome Glove™', icon: Hand, color: 'text-teal-400' },
    { id: 'clinicalvault', label: 'Clinical Data Vault', icon: Shield, color: 'text-emerald-400' },
    
    // Section: Community & Impact
    { id: 'community', label: 'Community Cloud (Basic)', icon: Globe, color: 'text-blue-400' },
    { id: 'communitymapping', label: 'Resilience Mapping', icon: Users, color: 'text-cyan-400' },
    
    // Section: Advanced Platform Features
    { id: 'advancedfeatures', label: 'Advanced Features', icon: Sparkles, color: 'text-purple-400' },
    
    // Section: Education & Sandbox
    { id: 'learn', label: 'Educational Portal', icon: GraduationCap, color: 'text-amber-400' },
    { id: 'sandbox', label: 'Simulation Sandbox', icon: Beaker, color: 'text-lime-400' },
    { id: 'future', label: 'Future Vision', icon: Rocket, color: 'text-rose-400' },
    { id: 'settings', label: 'Settings & Privacy', icon: Settings, color: 'text-slate-400' },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'home':
        return (
          <DashboardHome
            resilienceScore={resilienceScore}
            prediction={prediction}
            weeklyData={weeklyData}
            onStartSession={() => setActiveTab('monitor')}
          />
        );
      case 'monitor':
        return <MonitoringSession onComplete={handleCompleteSession} />;
      case 'train':
        return (
          <BiofeedbackGame
            userLevel={userProfile.level}
            userXP={userProfile.xp}
            streak={userProfile.streak}
          />
        );
      case 'twin':
        return <DigitalTwin currentSRI={resilienceScore.overall} />;
      case 'environment':
        return (
          <EnvironmentalFeedback
            environmentalData={environmentalData}
            currentSRI={resilienceScore.overall}
          />
        );
      case 'analysis':
        return <AnalysisDashboard sessions={sessions} />;
      case 'community':
        return <CommunityCloud communityData={communityData} />;
      case 'journal':
        return (
          <EmotionalJournal
            currentSRI={resilienceScore.overall}
            currentHRV={resilienceScore.hrv}
          />
        );
      case 'forecast':
        return (
          <ResilienceForecast
            currentSRI={resilienceScore.overall}
            historicalData={weeklyData}
          />
        );
      case 'cognitive':
        return <CognitiveGames currentSRI={resilienceScore.overall} />;
      case 'learn':
        return <EducationalPortal />;
      case 'sandbox':
        return <SimulationSandbox />;
      case 'future':
        return <FutureVision />;
      case 'settings':
        return <SettingsPrivacy />;
      case 'customstress':
        return <CustomStress />;
      case 'scientificanalysis':
        return <ScientificAnalysis />;
      case 'passivemonitoring':
        return <PassiveMonitoring />;
      
      // New Competition-Winning Features
      case 'predictive':
        return <AdvancedPredictiveEngine currentSRI={resilienceScore.overall} historicalData={weeklyData} />;
      case 'closedloop':
        return <ClosedLoopBiofeedback />;
      case 'nlpjournal':
        return <NLPJournaling />;
      case 'rqtracker':
        return <ResilienceQuotient currentSRI={resilienceScore.overall} sessions={sessions} />;
      case 'twinadvanced':
        return <DigitalTwinAdvanced currentSRI={resilienceScore.overall} />;
      case 'glove':
        return <GloveVisualization />;
      case 'clinicalvault':
        return <ClinicalDataVault />;
      case 'communitymapping':
        return <CommunityResilienceMap />;
      case 'advancedfeatures':
        return <AdvancedFeatures />;
      
      default:
        return (
          <DashboardHome
            resilienceScore={resilienceScore}
            prediction={prediction}
            weeklyData={weeklyData}
            onStartSession={() => setActiveTab('monitor')}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-foreground dark">
      <Toaster position="top-right" />

      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      {/* Header */}
      <header className="relative border-b border-slate-800 bg-slate-950/50 backdrop-blur-xl sticky top-0 z-40">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            {/* Logo and Menu Toggle */}
            <div className="flex items-center gap-3">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden"
              >
                {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </Button>
              
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-3"
              >
                <div className="relative">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-teal-400 to-cyan-500 flex items-center justify-center">
                    <Sparkles className="w-6 h-6 text-white" />
                  </div>
                  <motion.div
                    className="absolute inset-0 rounded-full bg-teal-400 blur-lg opacity-50"
                    animate={{
                      scale: [1, 1.2, 1],
                      opacity: [0.5, 0.3, 0.5],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: 'easeInOut',
                    }}
                  />
                </div>
                <div>
                  <h1 className="text-xl font-bold bg-gradient-to-r from-teal-400 to-cyan-500 bg-clip-text text-transparent">
                    Symbiome
                  </h1>
                  <p className="text-xs text-muted-foreground">Resilience Platform</p>
                </div>
              </motion.div>
            </div>

            {/* User Info */}
            <div className="flex items-center gap-4">
              <div className="hidden md:block text-right">
                <div className="text-sm font-semibold">{userProfile.name}</div>
                <div className="text-xs text-muted-foreground">Level {userProfile.level} • {userProfile.xp} XP</div>
              </div>
              <Badge variant="outline" className="px-3 py-1">
                {userProfile.streak} day streak 🔥
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Layout */}
      <div className="relative flex">
        {/* Vertical Sidebar Navigation */}
        <AnimatePresence>
          {(sidebarOpen || window.innerWidth >= 1024) && (
            <motion.aside
              initial={{ x: -300, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: -300, opacity: 0 }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              className="fixed lg:sticky top-[73px] left-0 h-[calc(100vh-73px)] w-80 border-r border-slate-800 bg-slate-950/50 backdrop-blur-xl z-30 lg:z-0"
            >
              <ScrollArea className="h-full">
                <div className="p-4 space-y-2">
                  <div className="px-3 py-2">
                    <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                      Navigation
                    </h2>
                  </div>
                  {navigationItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = activeTab === item.id;
                    return (
                      <motion.button
                        key={item.id}
                        onClick={() => {
                          setActiveTab(item.id);
                          if (window.innerWidth < 1024) {
                            setSidebarOpen(false);
                          }
                        }}
                        whileHover={{ scale: 1.02, x: 4 }}
                        whileTap={{ scale: 0.98 }}
                        className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg transition-all ${
                          isActive
                            ? 'bg-gradient-to-r from-teal-500/20 to-cyan-500/20 border border-teal-500/50'
                            : 'hover:bg-slate-800/50'
                        }`}
                      >
                        <Icon className={`w-5 h-5 ${isActive ? item.color : 'text-muted-foreground'}`} />
                        <span className={`flex-1 text-left text-sm ${isActive ? 'font-medium' : ''}`}>
                          {item.label}
                        </span>
                        {isActive && <ChevronRight className="w-4 h-4 text-teal-400" />}
                      </motion.button>
                    );
                  })}
                </div>
              </ScrollArea>
            </motion.aside>
          )}
        </AnimatePresence>

        {/* Main Content */}
        <main className="flex-1 relative">
          <div className="container mx-auto px-4 py-8 lg:px-8">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.2 }}
              >
                {renderContent()}
              </motion.div>
            </AnimatePresence>
          </div>
        </main>

        {/* Adaptive AI Coach - Floating Assistant */}
        <AdaptiveCoach
          currentSRI={resilienceScore.overall}
          show={showCoach}
          onDismiss={() => setShowCoach(false)}
        />
      </div>

      {/* Footer */}
      <footer className="relative border-t border-slate-800 bg-slate-950/50 backdrop-blur-xl mt-12">
        <div className="container mx-auto px-4 py-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-semibold mb-3 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-teal-400" />
                About Symbiome
              </h3>
              <p className="text-sm text-muted-foreground">
                An AI-enhanced, non-invasive biofeedback platform measuring how body and environment interact to shape stress and gut-related wellbeing.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-3">Core Features</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• HRV, GSR, Facial Calm tracking</li>
                <li>• Digital Twin AI prediction</li>
                <li>• Environmental correlation</li>
                <li>• Gut-brain axis logging</li>
                <li>• Gamified biofeedback</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-3">Research Ethics</h3>
              <p className="text-sm text-muted-foreground mb-2">
                All data is anonymized and stored securely. This platform is designed for research and educational purposes.
              </p>
              <p className="text-xs text-teal-400">
                Privacy-first • Consent-driven • Transparent
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-3">Future Vision</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• Symbiome Glove (BLE wearable)</li>
                <li>• Cloud-based AI learning</li>
                <li>• Global resilience mapping</li>
                <li>• Clinical validation studies</li>
                <li>• School & workplace pilots</li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-6 border-t border-slate-800">
            <div className="text-center text-sm text-muted-foreground mb-4">
              <p className="font-semibold mb-2">🏆 Built for BTYSTE & Science Competition Excellence</p>
              <p className="text-xs">
                Multi-modal biometrics • AI prediction • Environmental correlation • Gut-brain research • Community health mapping
              </p>
            </div>
            <div className="text-center text-xs text-muted-foreground">
              <p>Symbiome Research Platform © 2025 • Advancing the science of human resilience</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
