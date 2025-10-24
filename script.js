const questions = [
  {
    id: 'domain',
    title: 'In welchem Fachbereich brauchst du neue Impulse?',
    description:
      'Wir ordnen deine Anfrage einem thematischen Cluster zu, um wirklich relevante Quellen zu finden.',
    options: [
      {
        value: 'management',
        title: 'Strategie & Leadership',
        description: 'Organisationen führen, Transformation gestalten, Verantwortung tragen.'
      },
      {
        value: 'technology',
        title: 'Technologie & IT-Architektur',
        description: 'Systemdesign, Digitalisierung, Software- und Datenkompetenz.'
      },
      {
        value: 'people',
        title: 'People & Organisation',
        description: 'Talententwicklung, New Work, Change-Kommunikation und Kultur.'
      },
      {
        value: 'research',
        title: 'Wissenschaft & Analyse',
        description: 'Empirische Studien, Methodenkompetenz und analytische Tiefe.'
      },
      {
        value: 'health',
        title: 'Gesundheit & Pflegeinnovation',
        description: 'Versorgungsmodelle, evidenzbasierte Praxis und Public Health.'
      }
    ]
  },
  {
    id: 'goal',
    title: 'Welches Ziel verfolgst du mit der Lektüre?',
    description:
      'Auf Basis des Fachbereichs entscheiden wir, ob Grundlagen, Best Practices oder Zukunftsmodelle priorisiert werden.',
    options: [
      {
        value: 'transform',
        title: 'Transformation vorantreiben',
        description: 'Strategische Weichen stellen, komplexe Veränderung steuern.'
      },
      {
        value: 'optimize',
        title: 'Prozesse verbessern',
        description: 'Operational Excellence, Skalierung und messbare Effizienz.'
      },
      {
        value: 'upskill',
        title: 'Fachwissen vertiefen',
        description: 'Theorien verdichten, Modelle verstehen, Expertise erweitern.'
      },
      {
        value: 'teach',
        title: 'Wissen weitergeben',
        description: 'Didaktik, Frameworks und Beispiele für Teams & Lehre.'
      }
    ]
  },
  {
    id: 'experience',
    title: 'Auf welchem Erfahrungsniveau bewegst du dich?',
    description:
      'Damit die Literatur sprachlich, methodisch und vom Anspruch zum Vorwissen passt.',
    options: [
      {
        value: 'entry',
        title: 'Professioneller Einstieg',
        description: 'Fundierte Grundlagen, klare Strukturen, gut nachvollziehbar.'
      },
      {
        value: 'advanced',
        title: 'Fortgeschritten',
        description: 'Vertiefung mit anspruchsvollen Konzepten und Fallbeispielen.'
      },
      {
        value: 'expert',
        title: 'Executive / Expert Level',
        description: 'State-of-the-Art, Meta-Analysen und High-Level-Diskurs.'
      }
    ]
  },
  {
    id: 'approach',
    title: 'Welche Art von Erkenntnissen suchst du?',
    description: 'Darauf bauen wir die methodische und argumentative Dramaturgie auf.',
    options: [
      {
        value: 'strategic',
        title: 'Strategische Modelle & Frameworks',
        description: 'Referenzmodelle, Roadmaps und Gestaltungsprinzipien.'
      },
      {
        value: 'operational',
        title: 'Operative Umsetzung & Tools',
        description: 'Playbooks, Checklisten und konkrete Instrumente.'
      },
      {
        value: 'researchDriven',
        title: 'Forschungs- & Datenorientiert',
        description: 'Studien, Metaanalysen, evidenzbasierte Empfehlungen.'
      },
      {
        value: 'caseStudy',
        title: 'Fallstudien & Erfahrungsberichte',
        description: 'Best Practices, Lessons Learned und narrative Einblicke.'
      }
    ]
  },
  {
    id: 'depth',
    title: 'Welche Tiefe erwartest du?',
    description: 'Von verdichteten Executive Summaries bis zu tiefgehenden Analysen.',
    options: [
      {
        value: 'concise',
        title: 'Kompakt & auf den Punkt',
        description: 'Verdichtete Quintessenzen, klare Handlungsimpulse.'
      },
      {
        value: 'structured',
        title: 'Strukturiert & praxisnah',
        description: 'Ausgewogene Balance aus Theorie, Beispielen und Umsetzung.'
      },
      {
        value: 'immersive',
        title: 'Tiefgreifend & analytisch',
        description: 'Dichte Argumentationen, umfangreiche Modelle, hohe Komplexität.'
      }
    ]
  },
  {
    id: 'methodology',
    title: 'Welche methodische Fundierung erwartest du?',
    description:
      'Aufbauend auf Erkenntnisstil und Tiefe priorisieren wir die wissenschaftliche Aufbereitung.',
    options: [
      {
        value: 'qualitative',
        title: 'Qualitative Tiefenanalysen',
        description: 'Narrative Fallstudien, Interviews, ethnografische Beobachtungen.'
      },
      {
        value: 'quantitative',
        title: 'Quantitative Modelle & Kennzahlen',
        description: 'Statistische Modelle, ökonometrische Tests, belastbare Datensätze.'
      },
      {
        value: 'mixed',
        title: 'Mixed-Methods & Triangulation',
        description: 'Verzahnt Daten, Praxisbeispiele und reflektierte Theoriearbeit.'
      },
      {
        value: 'conceptual',
        title: 'Theorie- und Modellbildung',
        description: 'Konzeptionelle Frameworks, normative Leitplanken, begriffliche Schärfung.'
      }
    ]
  },
  {
    id: 'evidence',
    title: 'Wie möchtest du überzeugt werden?',
    description: 'Wir matchen auf deine bevorzugte Evidenzbasis und stärken sie methodisch.',
    options: [
      {
        value: 'data',
        title: 'Daten & Studien',
        description: 'Quantitative Analysen, Statistiken, harte Kennzahlen.'
      },
      {
        value: 'cases',
        title: 'Case Studies',
        description: 'Detaillierte Praxisbeispiele mit messbaren Ergebnissen.'
      },
      {
        value: 'frameworks',
        title: 'Frameworks & Modelle',
        description: 'Referenzarchitekturen, Reifegradmodelle, strukturierte Denkrahmen.'
      },
      {
        value: 'trends',
        title: 'Trends & Szenarien',
        description: 'Vorausschauende Analysen, Zukunftsbilder, foresight-getrieben.'
      }
    ]
  },
  {
    id: 'transfer',
    title: 'Wie soll das Wissen angewendet werden?',
    description: 'Nach der Evidenzpräferenz wählen wir die passende Transferarchitektur.',
    options: [
      {
        value: 'strategyBlueprints',
        title: 'Strategische Blaupausen',
        description: 'Roadmaps für Transformation, Portfolio- und Geschäftsmodellentscheidungen.'
      },
      {
        value: 'capabilityBuilding',
        title: 'Capability-Building Programme',
        description: 'Trainingsdesigns, Kompetenzpfade und Enablement-Formate.'
      },
      {
        value: 'innovationLab',
        title: 'Experiment & Prototyping',
        description: 'Hypothesentests, Innovation Accounting und Lab-Methoden.'
      },
      {
        value: 'governance',
        title: 'Governance & Policy Design',
        description: 'Regulatorische Leitplanken, Compliance-Mechaniken, Qualitätsstandards.'
      }
    ]
  },
  {
    id: 'context',
    title: 'In welchem organisationalen Kontext setzt du das Wissen ein?',
    description:
      'So können wir abschätzen, ob Skalierung, Regulatorik oder agile Lernzyklen im Vordergrund stehen.',
    options: [
      {
        value: 'enterprise',
        title: 'Konzern & reguliertes Umfeld',
        description: 'Mehrere Hierarchien, Stakeholder-Gremien, Compliance-Druck.'
      },
      {
        value: 'scaleup',
        title: 'Scale-up & wachsendes Unternehmen',
        description: 'Schnelles Wachstum, iteratives Arbeiten, Fokus auf Produkt-Markt-Fit.'
      },
      {
        value: 'publicSector',
        title: 'Öffentlicher Sektor / NGO',
        description: 'Politische Legitimation, Wirkung auf Systeme, gesellschaftlicher Auftrag.'
      },
      {
        value: 'researchLab',
        title: 'Forschungs- & Innovationslabor',
        description: 'Interdisziplinäre Teams, Prototyping, akademische Kooperationen.'
      }
    ]
  },
  {
    id: 'format',
    title: 'Welches Lernformat unterstützt dich am besten?',
    description: 'Von Handbüchern bis zu analytischen Erzählungen – wir passen den Stil an.',
    options: [
      {
        value: 'playbook',
        title: 'Playbook & Umsetzungsleitfaden',
        description: 'Schritt-für-Schritt, Templates, sofortige Anwendung.'
      },
      {
        value: 'handbook',
        title: 'Handbuch & Referenz',
        description: 'Umfassende Kompendien zum Nachschlagen und Vertiefen.'
      },
      {
        value: 'narrative',
        title: 'Narrative Analyse',
        description: 'Storytelling, Perspektivwechsel, reflektierende Essays.'
      },
      {
        value: 'academic',
        title: 'Akademisch & methodisch',
        description: 'Peer-Review-Niveau, Methodendiskussion, Theoriearbeit.'
      }
    ]
  },
  {
    id: 'timeHorizon',
    title: 'Welchen Wirkungshorizont hast du im Blick?',
    description: 'Wir berücksichtigen, ob du schnelle Impulse oder langfristige Transformationen planst.',
    options: [
      {
        value: 'quickWins',
        title: 'Quick Wins (0–3 Monate)',
        description: 'Schnell umsetzbare Maßnahmen, unmittelbare Wirkung.'
      },
      {
        value: 'midTerm',
        title: 'Mittelfristig (3–12 Monate)',
        description: 'Iterative Skalierung, Etablierung neuer Routinen.'
      },
      {
        value: 'longTerm',
        title: 'Langfristig (12+ Monate)',
        description: 'Systemische Veränderung, kulturelle und strukturelle Transformation.'
      }
    ]
  },
  {
    id: 'length',
    title: 'Wie viel Zeit kannst du investieren?',
    description: 'Wir berücksichtigen Umfang, Dichte und Lesedauer.',
    options: [
      {
        value: 'short',
        title: 'Verdichtet',
        description: 'Bis 220 Seiten bzw. sehr konzentrierte Formate.'
      },
      {
        value: 'medium',
        title: 'Ausgewogen',
        description: '250–420 Seiten, solide Lesedauer mit Tiefgang.'
      },
      {
        value: 'long',
        title: 'Umfassend',
        description: 'Über 420 Seiten oder modulare Sammelbände.'
      }
    ]
  },
  {
    id: 'insight',
    title: 'Welche Reflexionsebene soll das Werk erreichen?',
    description: 'Zum Abschluss definieren wir die Tiefe der wissenschaftlichen und praktischen Reflexion.',
    options: [
      {
        value: 'metaAnalysis',
        title: 'Meta-Analyse & Synthese',
        description: 'Verdichtet Studien, Modelle und Evidenzlandschaften systematisch.'
      },
      {
        value: 'criticalReflection',
        title: 'Kritische Reflexion',
        description: 'Hinterfragt Paradigmen, beleuchtet Ambivalenzen und Nebenwirkungen.'
      },
      {
        value: 'pragmaticPlaybook',
        title: 'Pragmatischer Implementierungsleitfaden',
        description: 'Fokussiert auf Roadmaps, Verantwortlichkeiten und Steuerungsgrößen.'
      },
      {
        value: 'narrativeCase',
        title: 'Narratives Fallarchiv',
        description: 'Verwebt dichte Praxisgeschichten mit analytischer Kommentierung.'
      }
    ]
  }
];

const bookDatabase = [
  {
    id: 'leading-change',
    title: 'Leading Change',
    author: 'John P. Kotter',
    type: 'fachliteratur',
    domain: ['management', 'people'],
    goal: ['transform', 'teach'],
    experience: ['entry', 'advanced'],
    approach: ['strategic', 'caseStudy'],
    depth: 'structured',
    methodology: ['qualitative', 'conceptual'],
    evidence: ['frameworks', 'cases'],
    transfer: ['strategyBlueprints', 'capabilityBuilding'],
    context: ['enterprise', 'publicSector'],
    format: ['handbook', 'playbook'],
    timeHorizon: ['midTerm', 'longTerm'],
    length: 'medium',
    insight: 'pragmaticPlaybook',
    description:
      'Kotter liefert einen präzisen Fahrplan für Veränderungsprozesse – von der Dringlichkeitsanalyse bis zur kulturellen Verankerung.',
    image: 'https://images.unsplash.com/photo-1485217988980-11786ced9454?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'devops-handbook',
    title: 'The DevOps Handbook',
    author: 'Gene Kim u. a.',
    type: 'fachliteratur',
    domain: ['technology', 'management'],
    goal: ['optimize', 'transform'],
    experience: ['advanced'],
    approach: ['operational', 'strategic'],
    depth: 'immersive',
    methodology: ['mixed', 'quantitative'],
    evidence: ['cases', 'data'],
    transfer: ['innovationLab', 'capabilityBuilding'],
    context: ['scaleup', 'enterprise'],
    format: ['playbook', 'handbook'],
    timeHorizon: ['midTerm', 'longTerm'],
    length: 'long',
    insight: 'pragmaticPlaybook',
    description:
      'Ein tiefes Kompendium über Continuous Delivery, Plattformteams und Metriken – gespickt mit Erfahrungen führender Tech-Unternehmen.',
    image: 'https://images.unsplash.com/photo-1517430816045-df4b7de11d1d?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'ddia',
    title: 'Designing Data-Intensive Applications',
    author: 'Martin Kleppmann',
    type: 'fachliteratur',
    domain: ['technology', 'research'],
    goal: ['upskill', 'teach'],
    experience: ['expert'],
    approach: ['researchDriven', 'strategic'],
    depth: 'immersive',
    methodology: ['quantitative', 'conceptual'],
    evidence: ['data', 'frameworks'],
    transfer: ['innovationLab', 'strategyBlueprints'],
    context: ['scaleup', 'enterprise', 'researchLab'],
    format: ['handbook', 'academic'],
    timeHorizon: ['longTerm'],
    length: 'long',
    insight: 'metaAnalysis',
    description:
      'Kleppmann analysiert Architekturen verteilter Systeme, Datenmodelle und Skalierungsstrategien – ein Standardwerk für technische Entscheider:innen.',
    image: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'reinventing-organizations',
    title: 'Reinventing Organizations',
    author: 'Frederic Laloux',
    type: 'fachliteratur',
    domain: ['people', 'management'],
    goal: ['transform', 'teach'],
    experience: ['advanced'],
    approach: ['strategic', 'caseStudy'],
    depth: 'structured',
    methodology: ['qualitative', 'mixed'],
    evidence: ['cases', 'trends'],
    transfer: ['capabilityBuilding', 'governance'],
    context: ['scaleup', 'publicSector'],
    format: ['narrative', 'handbook'],
    timeHorizon: ['midTerm', 'longTerm'],
    length: 'medium',
    insight: 'criticalReflection',
    description:
      'Eine umfassende Analyse selbstorganisierter Unternehmen mit praxisnahen Beispielen und konkreten Gestaltungsprinzipien.',
    image: 'https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'lean-analytics',
    title: 'Lean Analytics',
    author: 'Alistair Croll & Benjamin Yoskovitz',
    type: 'fachliteratur',
    domain: ['technology', 'research'],
    goal: ['optimize', 'upskill'],
    experience: ['advanced'],
    approach: ['operational', 'researchDriven'],
    depth: 'structured',
    methodology: ['quantitative', 'mixed'],
    evidence: ['data', 'cases'],
    transfer: ['innovationLab', 'strategyBlueprints'],
    context: ['scaleup', 'enterprise'],
    format: ['playbook'],
    timeHorizon: ['quickWins', 'midTerm'],
    length: 'medium',
    insight: 'pragmaticPlaybook',
    description:
      'Zeigt, wie datengetriebenes Arbeiten Produktentscheidungen verbessert – mit konkreten KPI-Modellen für jede Wachstumsphase.',
    image: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'digital-transformation-playbook',
    title: 'The Digital Transformation Playbook',
    author: 'David L. Rogers',
    type: 'fachliteratur',
    domain: ['management', 'technology'],
    goal: ['transform'],
    experience: ['entry', 'advanced'],
    approach: ['strategic'],
    depth: 'structured',
    methodology: ['conceptual', 'mixed'],
    evidence: ['frameworks', 'trends'],
    transfer: ['strategyBlueprints', 'capabilityBuilding'],
    context: ['enterprise', 'scaleup'],
    format: ['handbook', 'playbook'],
    timeHorizon: ['midTerm', 'longTerm'],
    length: 'medium',
    insight: 'pragmaticPlaybook',
    description:
      'Rogers verbindet Geschäftsmodellinnovation, Kundenzentrierung und Plattformlogiken zu einer klaren Transformationsagenda.',
    image: 'https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'value-based-healthcare',
    title: 'Redefining Health Care',
    author: 'Michael E. Porter & Elizabeth Olmsted Teisberg',
    type: 'fachliteratur',
    domain: ['health', 'management'],
    goal: ['transform', 'optimize'],
    experience: ['expert'],
    approach: ['researchDriven', 'strategic'],
    depth: 'immersive',
    methodology: ['quantitative', 'conceptual'],
    evidence: ['data', 'frameworks'],
    transfer: ['governance', 'strategyBlueprints'],
    context: ['enterprise', 'publicSector'],
    format: ['academic', 'handbook'],
    timeHorizon: ['longTerm'],
    length: 'long',
    insight: 'metaAnalysis',
    description:
      'Ein Referenzwerk für Value-Based Healthcare mit präzisen Kennzahlensystemen und praxisnahen Implementierungspfaden.',
    image: 'https://images.unsplash.com/photo-1587502536240-183035fb2d1d?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'evidence-based-management',
    title: 'Hard Facts, Dangerous Half-Truths & Total Nonsense',
    author: 'Jeffrey Pfeffer & Robert I. Sutton',
    type: 'fachliteratur',
    domain: ['management', 'research'],
    goal: ['upskill', 'teach'],
    experience: ['entry', 'advanced'],
    approach: ['researchDriven'],
    depth: 'structured',
    methodology: ['mixed', 'quantitative'],
    evidence: ['data', 'frameworks'],
    transfer: ['governance', 'capabilityBuilding'],
    context: ['enterprise', 'publicSector'],
    format: ['narrative', 'academic'],
    timeHorizon: ['midTerm'],
    length: 'medium',
    insight: 'criticalReflection',
    description:
      'Zeigt, wie Managemententscheidungen konsequent auf Evidenz basieren – mit klaren Kriterien zur Bewertung von Studien und Best Practices.',
    image: 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'fearless-organization',
    title: 'The Fearless Organization',
    author: 'Amy C. Edmondson',
    type: 'fachliteratur',
    domain: ['people', 'management'],
    goal: ['transform', 'optimize'],
    experience: ['advanced'],
    approach: ['caseStudy', 'strategic'],
    depth: 'structured',
    methodology: ['qualitative', 'mixed'],
    evidence: ['cases', 'frameworks'],
    transfer: ['capabilityBuilding', 'governance'],
    context: ['scaleup', 'enterprise'],
    format: ['handbook', 'narrative'],
    timeHorizon: ['midTerm', 'longTerm'],
    length: 'medium',
    insight: 'narrativeCase',
    description:
      'Edmondson erklärt, wie psychologische Sicherheit Leistung und Innovation steigert – mit diagnostischen Tools und Interventionsempfehlungen.',
    image: 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'systems-leadership',
    title: 'The Fifth Discipline: Systems Thinking in Practice',
    author: 'Peter M. Senge',
    type: 'fachliteratur',
    domain: ['management', 'people'],
    goal: ['transform', 'teach'],
    experience: ['advanced', 'expert'],
    approach: ['strategic', 'researchDriven'],
    depth: 'immersive',
    methodology: ['conceptual', 'mixed'],
    evidence: ['frameworks', 'trends'],
    transfer: ['governance', 'strategyBlueprints'],
    context: ['enterprise', 'publicSector'],
    format: ['handbook', 'academic'],
    timeHorizon: ['longTerm'],
    length: 'long',
    insight: 'metaAnalysis',
    description:
      'Senge illustriert, wie systemisches Denken komplexe Veränderungsprozesse ermöglicht – mit Archetypen, Lernarchitekturen und Governance-Prinzipien.',
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 'mission-economy',
    title: 'Mission Economy',
    author: 'Mariana Mazzucato',
    type: 'fachliteratur',
    domain: ['health', 'management'],
    goal: ['transform', 'teach'],
    experience: ['advanced'],
    approach: ['strategic', 'caseStudy'],
    depth: 'structured',
    methodology: ['mixed', 'conceptual'],
    evidence: ['trends', 'cases'],
    transfer: ['governance', 'strategyBlueprints'],
    context: ['publicSector', 'enterprise'],
    format: ['narrative', 'handbook'],
    timeHorizon: ['midTerm', 'longTerm'],
    length: 'medium',
    insight: 'criticalReflection',
    description:
      'Mazzucato zeigt, wie staatliche und gesellschaftliche Akteur:innen missionsorientierte Innovationen orchestrieren – mit Beispielen aus Gesundheits-, Klima- und Technologiefeldern.',
    image: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=700&q=82'
  },
  {
    id: 'designing-for-digital',
    title: 'Designed for Digital',
    author: 'Jeanne W. Ross, Cynthia M. Beath & Martin Mocker',
    type: 'fachliteratur',
    domain: ['technology', 'management'],
    goal: ['transform', 'optimize'],
    experience: ['advanced', 'expert'],
    approach: ['strategic', 'operational'],
    depth: 'structured',
    methodology: ['mixed', 'conceptual'],
    evidence: ['frameworks', 'cases'],
    transfer: ['strategyBlueprints', 'capabilityBuilding'],
    context: ['enterprise', 'scaleup'],
    format: ['handbook'],
    timeHorizon: ['midTerm', 'longTerm'],
    length: 'medium',
    insight: 'pragmaticPlaybook',
    description:
      'Ross und Kolleg:innen beschreiben Plattformarchitekturen, modulare Operating Models und Governance-Mechanismen für digitale Unternehmen.',
    image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=700&q=80'
  }
];

const answers = {};
let currentIndex = 0;

const startBtn = document.getElementById('startQuiz');
const questionCard = document.getElementById('questionCard');
const resultCard = document.getElementById('resultCard');
const optionGrid = document.getElementById('optionGrid');
const stepLabel = document.getElementById('stepLabel');
const progressBar = document.getElementById('progressBar');
const questionTitle = document.getElementById('questionTitle');
const questionDesc = document.getElementById('questionDesc');
const nextBtn = document.getElementById('nextBtn');
const backBtn = document.getElementById('backBtn');
const restartBtn = document.getElementById('restartBtn');
const resultImage = document.getElementById('resultImage');
const resultTitle = document.getElementById('resultTitle');
const resultMeta = document.getElementById('resultMeta');
const resultDescription = document.getElementById('resultDescription');
const resultHighlights = document.getElementById('resultHighlights');
const resultSynthesis = document.getElementById('resultSynthesis');
const resultNextSteps = document.getElementById('resultNextSteps');

startBtn.addEventListener('click', () => {
  document.querySelector('.hero').scrollIntoView({ behavior: 'smooth', block: 'start' });
  startBtn.setAttribute('disabled', 'true');
  questionCard.hidden = false;
  renderQuestion();
});

nextBtn.addEventListener('click', () => {
  const currentQuestion = questions[currentIndex];
  if (!answers[currentQuestion.id]) {
    shakeCard(questionCard);
    return;
  }
  currentIndex += 1;
  if (currentIndex >= questions.length) {
    showResults();
  } else {
    renderQuestion();
  }
});

backBtn.addEventListener('click', () => {
  if (currentIndex === 0) return;
  currentIndex -= 1;
  renderQuestion();
});

restartBtn.addEventListener('click', resetQuiz);

function renderQuestion() {
  const question = questions[currentIndex];
  questionTitle.textContent = question.title;
  questionDesc.textContent = question.description;
  stepLabel.textContent = `Frage ${currentIndex + 1} von ${questions.length}`;
  progressBar.style.width = `${(currentIndex / questions.length) * 100}%`;

  optionGrid.innerHTML = '';
  question.options.forEach(option => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'option';
    if (answers[question.id] === option.value) {
      button.classList.add('selected');
    }
    button.innerHTML = `
      <span class="option-title">${option.title}</span>
      <span class="option-desc">${option.description}</span>
    `;
    button.addEventListener('click', () => {
      answers[question.id] = option.value;
      [...optionGrid.children].forEach(child => child.classList.remove('selected'));
      button.classList.add('selected');
      nextBtn.focus();
    });
    optionGrid.appendChild(button);
  });

  backBtn.hidden = currentIndex === 0;
  nextBtn.textContent = currentIndex === questions.length - 1 ? 'Ergebnis anzeigen' : 'Weiter';
}

function shakeCard(element) {
  element.animate(
    [
      { transform: 'translateX(0)' },
      { transform: 'translateX(-8px)' },
      { transform: 'translateX(8px)' },
      { transform: 'translateX(-4px)' },
      { transform: 'translateX(0)' }
    ],
    {
      duration: 400,
      easing: 'ease-in-out'
    }
  );
}

async function fetchBooksFromDatabase() {
  return new Promise(resolve => {
    setTimeout(() => resolve(JSON.parse(JSON.stringify(bookDatabase))), 320);
  });
}

async function showResults() {
  progressBar.style.width = '100%';
  questionCard.hidden = true;
  resultCard.hidden = false;
  resultCard.classList.add('active');

  const entries = await fetchBooksFromDatabase();
  const match = rankEntries(entries, answers);
  presentResult(match, answers);
}

function matchesPreference(entryValue, filterValue) {
  if (!entryValue || !filterValue) return false;
  if (Array.isArray(entryValue)) {
    return entryValue.includes(filterValue);
  }
  return entryValue === filterValue;
}

function rankEntries(entries, filters) {
  let best = null;
  let bestScore = -Infinity;

  entries.forEach(entry => {
    let score = 0;
    const highlights = [];

    if (matchesPreference(entry.domain, filters.domain)) {
      score += 2.6;
      highlights.push(`✔️ Fachfokus: <strong>${domainLabel(filters.domain)}</strong> adressiert dein Vorhaben.`);
    }

    if (matchesPreference(entry.goal, filters.goal)) {
      score += 2.3;
      highlights.push(`✔️ Zielbild „${goalLabel(filters.goal)}“ wird direkt unterstützt.`);
    }

    if (matchesPreference(entry.experience, filters.experience)) {
      score += 1.9;
      highlights.push(`✔️ Anspruchsniveau: <strong>${experienceLabel(filters.experience)}</strong>.`);
      if (filters.experience === 'expert' && matchesPreference(entry.depth, 'immersive')) {
        score += 0.3;
      }
    }

    if (matchesPreference(entry.approach, filters.approach)) {
      score += 2.0;
      highlights.push(`✔️ Erkenntnisstil auf <strong>${approachLabel(filters.approach)}</strong> ausgerichtet.`);
    }

    if (matchesPreference(entry.depth, filters.depth)) {
      score += 1.6;
      highlights.push(`✔️ Tiefe entspricht deinem Wunsch nach <strong>${depthLabel(filters.depth)}</strong>.`);
    }

    if (matchesPreference(entry.methodology, filters.methodology)) {
      score += 1.4;
      highlights.push(`✔️ Methodische Fundierung basiert auf <strong>${methodologyLabel(filters.methodology)}</strong>.`);
      if (filters.methodology === 'mixed' && matchesPreference(entry.evidence, filters.evidence)) {
        score += 0.2;
      }
    }

    if (matchesPreference(entry.evidence, filters.evidence)) {
      score += 1.5;
      highlights.push(`✔️ Evidenzform: <strong>${evidenceLabel(filters.evidence)}</strong>.`);
    }

    if (matchesPreference(entry.transfer, filters.transfer)) {
      score += 1.3;
      highlights.push(`✔️ Transferpfad: <strong>${transferLabel(filters.transfer)}</strong>.`);
    }

    if (matchesPreference(entry.context, filters.context)) {
      score += 1.7;
      highlights.push(`✔️ Umsetzungskontext <strong>${contextLabel(filters.context)}</strong> wird adressiert.`);
    }

    if (matchesPreference(entry.format, filters.format)) {
      score += 1.2;
      highlights.push(`✔️ Lernformat <strong>${formatLabel(filters.format)}</strong> passt zu dir.`);
    }

    if (matchesPreference(entry.timeHorizon, filters.timeHorizon)) {
      score += 1.1;
      highlights.push(`✔️ Wirkungshorizont <strong>${timeHorizonLabel(filters.timeHorizon)}</strong>.`);
      if (filters.timeHorizon === 'quickWins' && matchesPreference(entry.format, 'playbook')) {
        score += 0.2;
      }
    }

    if (entry.length === filters.length) {
      score += 0.9;
      highlights.push(`✔️ Umfang bleibt innerhalb <strong>${lengthLabel(filters.length)}</strong>.`);
    }

    if (matchesPreference(entry.insight, filters.insight)) {
      score += 1.1;
      highlights.push(`✔️ Reflexionsebene: <strong>${insightLabel(filters.insight)}</strong>.`);
    }

    if (entry.type === 'fachliteratur') {
      score += 0.4;
    }

    if (score > bestScore) {
      bestScore = score;
      best = { entry, highlights };
    }
  });

  return best;
}

function presentResult(result, filters) {
  if (!result) return;
  const { entry, highlights } = result;

  resultImage.src = entry.image;
  resultTitle.textContent = `${entry.title}`;
  const primaryDomain = Array.isArray(entry.domain) ? entry.domain[0] : entry.domain;
  const domainText = primaryDomain ? domainLabel(primaryDomain) : 'Interdisziplinär';
  resultMeta.innerHTML = `von ${entry.author} · Fachliteratur · ${domainText}`;
  resultDescription.textContent = entry.description;
  resultSynthesis.innerHTML = craftSynthesis(entry, filters);
  resultHighlights.innerHTML = highlights.map(item => `<span>${item}</span>`).join('');
  const steps = buildNextSteps(entry, filters);
  resultNextSteps.innerHTML = steps.map(step => `<li>${step}</li>`).join('');
  restartBtn.focus();
}

function craftSynthesis(entry, filters) {
  const domainValue = filters.domain || (Array.isArray(entry.domain) ? entry.domain[0] : entry.domain);
  const goalValue = filters.goal || (Array.isArray(entry.goal) ? entry.goal[0] : entry.goal);
  const contextValue = filters.context || (Array.isArray(entry.context) ? entry.context[0] : entry.context);
  const approachValue = filters.approach || (Array.isArray(entry.approach) ? entry.approach[0] : entry.approach);
  const methodologyValue = filters.methodology || (Array.isArray(entry.methodology) ? entry.methodology[0] : entry.methodology);
  const evidenceValue = filters.evidence || (Array.isArray(entry.evidence) ? entry.evidence[0] : entry.evidence);
  const depthValue = filters.depth || entry.depth;
  const insightValue = filters.insight || entry.insight;
  const timeValue = filters.timeHorizon || (Array.isArray(entry.timeHorizon) ? entry.timeHorizon[0] : entry.timeHorizon);

  const fragments = [];
  const contextSnippet = contextValue ? ` im Kontext <strong>${contextLabel(contextValue)}</strong>` : '';
  const domainSnippet = domainValue ? `<strong>${domainLabel(domainValue)}</strong>` : 'deinem Themenfeld';
  const goalSnippet = goalValue ? ` mit dem Ziel „${goalLabel(goalValue)}“` : '';
  fragments.push(`Das Werk verschränkt ${domainSnippet}${goalSnippet}${contextSnippet} und liefert einen kuratierten Orientierungsrahmen.`);

  const approachSnippet = approachValue ? `<strong>${approachLabel(approachValue)}</strong>` : 'mehrere Perspektiven';
  const evidenceSnippet = evidenceValue ? `<strong>${evidenceLabel(evidenceValue)}</strong>` : 'relevanten Quellen';
  const methodologySnippet = methodologyValue ? `<strong>${methodologyLabel(methodologyValue)}</strong>` : 'einer ausgewogenen Methodik';
  fragments.push(`Es kombiniert ${approachSnippet} mit Evidenzen aus ${evidenceSnippet} und stützt sich methodisch auf ${methodologySnippet}.`);

  const depthSnippet = depthValue ? depthLabel(depthValue).toLowerCase() : 'präzise';
  const insightSnippet = insightValue ? `<strong>${insightLabel(insightValue)}</strong>` : 'tiefe Reflexion';
  const timeSnippet = timeValue ? ` entlang des Horizonts <strong>${timeHorizonLabel(timeValue)}</strong>` : '';
  fragments.push(`Erwarte eine ${depthSnippet} Aufbereitung, die auf ${insightSnippet} zielt${timeSnippet}.`);

  return fragments.map(text => `<p>${text}</p>`).join('');
}

function buildNextSteps(entry, filters) {
  const steps = [];
  const goalValue = filters.goal || (Array.isArray(entry.goal) ? entry.goal[0] : entry.goal);
  const transferValue = filters.transfer || (Array.isArray(entry.transfer) ? entry.transfer[0] : entry.transfer);
  const formatValue = filters.format || (Array.isArray(entry.format) ? entry.format[0] : entry.format);
  const timeValue = filters.timeHorizon || (Array.isArray(entry.timeHorizon) ? entry.timeHorizon[0] : entry.timeHorizon);
  const methodologyValue = filters.methodology || (Array.isArray(entry.methodology) ? entry.methodology[0] : entry.methodology);
  const evidenceValue = filters.evidence || (Array.isArray(entry.evidence) ? entry.evidence[0] : entry.evidence);
  const contextValue = filters.context || (Array.isArray(entry.context) ? entry.context[0] : entry.context);

  if (goalValue) {
    steps.push(`Starte mit einem Kick-off, in dem du das Ziel „${goalLabel(goalValue)}“ und den Nutzen für alle Stakeholder klar machst.`);
  }

  if (transferValue || formatValue) {
    const pieces = [];
    if (transferValue) pieces.push(`Transferartefakte für ${transferLabel(transferValue)}`);
    if (formatValue) pieces.push(`das Format ${formatLabel(formatValue)}`);
    steps.push(`Arbeite Kapitelsynopsen heraus und übersetze sie in ${pieces.join(' und ')}.`);
  }

  if (methodologyValue || evidenceValue) {
    const details = [];
    if (methodologyValue) details.push(`Methodik (${methodologyLabel(methodologyValue)})`);
    if (evidenceValue) details.push(`Evidenzen (${evidenceLabel(evidenceValue)})`);
    steps.push(`Dokumentiere ${details.join(' & ')} in einem Research-Log, damit Entscheidungen nachvollziehbar bleiben.`);
  }

  if (timeValue) {
    steps.push(`Setze Review-Meilensteine entlang des Horizonts ${timeHorizonLabel(timeValue)} und verbinde sie mit klaren Entscheidungspunkten.`);
  }

  if (contextValue) {
    steps.push(`Binde Schlüsselpersonen aus dem Kontext ${contextLabel(contextValue)} über Co-Creation-Sessions und Feedback-Loops ein.`);
  }

  return steps.slice(0, 4);
}

function resetQuiz() {
  Object.keys(answers).forEach(key => delete answers[key]);
  currentIndex = 0;
  resultCard.hidden = true;
  resultCard.classList.remove('active');
  questionCard.hidden = false;
  progressBar.style.width = '0%';
  nextBtn.textContent = 'Weiter';
  resultHighlights.innerHTML = '';
  resultSynthesis.innerHTML = '';
  resultNextSteps.innerHTML = '';
  renderQuestion();
}

function domainLabel(value) {
  return {
    management: 'Strategie & Leadership',
    technology: 'Technologie & IT-Architektur',
    people: 'People & Organisation',
    research: 'Wissenschaft & Analyse',
    health: 'Gesundheit & Pflegeinnovation'
  }[value] || value;
}

function goalLabel(value) {
  return {
    transform: 'Transformation vorantreiben',
    optimize: 'Prozesse verbessern',
    upskill: 'Fachwissen vertiefen',
    teach: 'Wissen weitergeben'
  }[value] || value;
}

function experienceLabel(value) {
  return {
    entry: 'Professioneller Einstieg',
    advanced: 'Fortgeschritten',
    expert: 'Executive / Expert Level'
  }[value] || value;
}

function approachLabel(value) {
  return {
    strategic: 'Strategische Modelle & Frameworks',
    operational: 'Operative Umsetzung & Tools',
    researchDriven: 'Forschungs- & Datenorientiert',
    caseStudy: 'Fallstudien & Erfahrungsberichte'
  }[value] || value;
}

function depthLabel(value) {
  return {
    concise: 'Kompakt & auf den Punkt',
    structured: 'Strukturiert & praxisnah',
    immersive: 'Tiefgreifend & analytisch'
  }[value] || value;
}

function methodologyLabel(value) {
  return {
    qualitative: 'qualitativen Tiefenanalysen',
    quantitative: 'quantitativen Wirkungsnachweisen',
    mixed: 'kombinierten Mixed-Methods-Designs',
    conceptual: 'theoretischer Modellbildung'
  }[value] || value;
}

function evidenceLabel(value) {
  return {
    data: 'Daten & Studien',
    cases: 'Case Studies',
    frameworks: 'Frameworks & Modelle',
    trends: 'Trends & Szenarien'
  }[value] || value;
}

function transferLabel(value) {
  return {
    strategyBlueprints: 'strategische Blaupausen',
    capabilityBuilding: 'Capability-Building-Initiativen',
    innovationLab: 'experimentelle Innovationsarbeit',
    governance: 'Governance- & Policy-Strukturen'
  }[value] || value;
}

function contextLabel(value) {
  return {
    enterprise: 'Konzern & reguliertes Umfeld',
    scaleup: 'Scale-up & wachsendes Unternehmen',
    publicSector: 'Öffentlicher Sektor / NGO',
    researchLab: 'Forschungs- & Innovationslabor'
  }[value] || value;
}

function formatLabel(value) {
  return {
    playbook: 'Playbook & Umsetzungsleitfaden',
    handbook: 'Handbuch & Referenz',
    narrative: 'Narrative Analyse',
    academic: 'Akademisch & methodisch'
  }[value] || value;
}

function lengthLabel(value) {
  return {
    short: 'einer verdichteten Lektüre',
    medium: 'eines ausgewogenen Umfangs',
    long: 'einer umfassenden Vertiefung'
  }[value] || value;
}

function insightLabel(value) {
  return {
    metaAnalysis: 'Meta-Analyse & Synthese',
    criticalReflection: 'kritischer Reflexion',
    pragmaticPlaybook: 'pragmatischem Implementierungsleitfaden',
    narrativeCase: 'narrativem Fallarchiv'
  }[value] || value;
}

function timeHorizonLabel(value) {
  return {
    quickWins: 'Quick Wins (0–3 Monate)',
    midTerm: 'Mittelfristig (3–12 Monate)',
    longTerm: 'Langfristig (12+ Monate)'
  }[value] || value;
}
