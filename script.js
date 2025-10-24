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
    format: ['handbook', 'playbook'],
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
    format: ['playbook', 'handbook'],
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
    format: ['handbook', 'academic'],
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
    format: ['narrative', 'handbook'],
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
    format: ['playbook'],
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
    format: ['handbook', 'playbook'],
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
    format: ['academic', 'handbook'],
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
    format: ['narrative', 'academic'],
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
    format: ['handbook', 'narrative'],
    length: 'medium',
    insight: 'narrativeCase',
    description:
      'Edmondson erklärt, wie psychologische Sicherheit Leistung und Innovation steigert – mit diagnostischen Tools und Interventionsempfehlungen.',
    image: 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=700&q=80'
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
  presentResult(match);
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
      highlights.push(`✔️ Fachfokus <strong>${domainLabel(filters.domain)}</strong> trifft dein Anliegen.`);
    }

    if (matchesPreference(entry.goal, filters.goal)) {
      score += 2.3;
      highlights.push(`✔️ Unterstützt dein Ziel <strong>${goalLabel(filters.goal)}</strong>.`);
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
      highlights.push(`✔️ Erkenntnisstil: <strong>${approachLabel(filters.approach)}</strong>.`);
    }

    if (matchesPreference(entry.depth, filters.depth)) {
      score += 1.6;
      highlights.push(`✔️ Tiefe entspricht <strong>${depthLabel(filters.depth)}</strong>.`);
    }

    if (matchesPreference(entry.methodology, filters.methodology)) {
      score += 1.4;
      highlights.push(`✔️ Methodische Fundierung: <strong>${methodologyLabel(filters.methodology)}</strong>.`);
      if (filters.methodology === 'mixed' && matchesPreference(entry.evidence, filters.evidence)) {
        score += 0.2;
      }
    }

    if (matchesPreference(entry.evidence, filters.evidence)) {
      score += 1.5;
      highlights.push(`✔️ Belegt durch <strong>${evidenceLabel(filters.evidence)}</strong>.`);
    }

    if (matchesPreference(entry.transfer, filters.transfer)) {
      score += 1.3;
      highlights.push(`✔️ Transfer in Richtung <strong>${transferLabel(filters.transfer)}</strong>.`);
    }

    if (matchesPreference(entry.format, filters.format)) {
      score += 1.2;
      highlights.push(`✔️ Lernformat <strong>${formatLabel(filters.format)}</strong> passt zu dir.`);
    }

    if (entry.length === filters.length) {
      score += 0.9;
      highlights.push(`✔️ Umfang liegt im Bereich <strong>${lengthLabel(filters.length)}</strong>.`);
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

function presentResult(result) {
  if (!result) return;
  const { entry, highlights } = result;

  resultImage.src = entry.image;
  resultTitle.textContent = `${entry.title}`;
  const primaryDomain = Array.isArray(entry.domain) ? entry.domain[0] : entry.domain;
  const domainText = primaryDomain ? domainLabel(primaryDomain) : 'Interdisziplinär';
  resultMeta.innerHTML = `von ${entry.author} · Fachliteratur · ${domainText}`;
  resultDescription.textContent = entry.description;
  resultHighlights.innerHTML = highlights.map(item => `<span>${item}</span>`).join('');
  restartBtn.focus();
}

function resetQuiz() {
  Object.keys(answers).forEach(key => delete answers[key]);
  currentIndex = 0;
  resultCard.hidden = true;
  resultCard.classList.remove('active');
  questionCard.hidden = false;
  progressBar.style.width = '0%';
  nextBtn.textContent = 'Weiter';
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
    strategyBlueprints: 'strategischer Blaupausen',
    capabilityBuilding: 'Capability-Building-Initiativen',
    innovationLab: 'experimenteller Innovationsarbeit',
    governance: 'Governance- & Policy-Strukturen'
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
    short: 'verdichteter Lektüre',
    medium: 'ausgewogenem Umfang',
    long: 'umfassender Vertiefung'
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
