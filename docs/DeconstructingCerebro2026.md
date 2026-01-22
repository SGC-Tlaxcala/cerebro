# Technical Narrative: Cerebro – A Governance-Oriented Management System

## 1. System Characterization

Cerebro is a Django-based modular monolith that implements organizational governance as executable code. It protects institutional memory, enforces procedural compliance, and stabilizes operational workflows through structured documentation, corrective action tracking, and innovation capture.

This is not productivity tooling—it is accountability infrastructure. The system's purpose is to make process deviations visible, document decisions with full traceability, and ensure that regulatory or quality management obligations cannot be silently dropped. Failures would be costly not because of technical impact, but because they compromise audit trails, procedural evidence, or the ability to demonstrate compliance to external auditors.

The implementation reveals a system designed for an organization where documents are legal artifacts, where corrective actions must survive staff turnover, and where informal knowledge must be converted into institutional knowledge with minimal friction. It operates in the space between human judgment and mandatory record-keeping.

## 2. Architectural Reality

### Module Structure
The system implements domain separation through Django apps, but these boundaries are pragmatic rather than dogmatic:

```
- docs:      Quality Management System document repository
- pas:       Action plan tracking (CNC/PCM workflows)
- ideas:     Innovation capture and review
- profiles:  Organizational structure mapping
- kpi:       Campaign and metric tracking
- vozmac:    Additional domain (structure observed)
- carto:     Additional domain (structure observed)
- pmml:      Additional domain (structure observed)
```

Each app follows Django conventions strictly: models define entities, forms encode validation, views orchestrate workflows, and admin interfaces provide power-user access. The architecture does not innovate—it leverages Django's stability.

### Boundary Enforcement
Domain boundaries are enforced through foreign keys and user ownership, not through service contracts or API versioning. Cross-domain coupling happens at the database level. The `docs` app is conceptually central—other domains reference it—but there is no enforcement layer preventing backward dependencies if they emerge.

The system uses the ORM as its integration layer. This creates tight coupling at the data model level but maintains simplicity: changes propagate through migrations, not through versioned API contracts.

### What This Reveals
The architectural choices prioritize **operational continuity over modularity**. The system assumes:
- Deployments are infrequent and deliberate
- Schema migrations can be coordinated
- All components share a lifecycle
- The cost of distributed systems (versioning, network failures, eventual consistency) is higher than the cost of tight coupling

This is the architecture of a system that must remain operational for years without major rewrites, evolving incrementally under resource constraints.

## 3. Core Domains and Responsibility Boundaries

### Document Management (`docs`)
**Responsibility:** Maintain version-controlled, immutable records of organizational documents with full audit history.

**Invariants Owned:**
- Document-Revision uniqueness: `unique_together = (("documento", "revision"))`
- File integrity through SHA-256 checksums calculated on save
- Notification tracking to ensure distribution accountability
- Authorship and temporal traceability (author, created, updated on all entities)

**Dependencies Not Controlled:**
- User existence and authentication (depends on Django auth)
- File system reliability for document storage
- Email delivery for notifications (fire-and-forget)

**Enforcement Mechanism:**
- Database constraints enforce uniqueness
- Checksum calculation happens in model save, not externally
- Revision immutability is a convention, not enforced by code (no explicit read-only flag)
- Report resolution workflow is status-based but not state-machine validated

**Boundary Reality:** This domain assumes it is the source of truth for documents. Other domains reference documents but do not modify them. Revision history is append-only in practice, though the code does not prevent deletion through admin actions.

### Action Plan Tracking (`pas`)
**Responsibility:** Manage lifecycle of corrective (CNC) and preventive (PCM) action plans through formal review and closure.

**Invariants Owned:**
- Plan-Action-Seguimiento hierarchy (cascade deletes enforce structure)
- Status progression tracking through timestamps
- Responsibility assignment and tracking
- Temporal sequencing (fecha_inicio, fecha_fin, fecha_llenado)

**Dependencies Not Controlled:**
- Correct assignment of responsible users (assumes users exist and emails work)
- Temporal validity (no enforcement that follow-up dates are sequential)
- Complete evidence capture (file uploads optional, not validated)

**Enforcement Mechanism:**
- Foreign key constraints enforce relational integrity
- User injection happens in admin save hooks, not model-level
- State transitions inferred from most recent Seguimiento, not validated
- Closure fields (eliminacion, recurrencia) are flags, not workflow gates

**Boundary Reality:** The domain models organizational procedures but relies on human discipline for correctness. The code provides structure and traceability but does not prevent process violations. It records what happened, not what should happen.

### Innovation Management (`ideas`)
**Responsibility:** Capture employee suggestions and management responses with minimal friction.

**Invariants Owned:**
- Idea uniqueness by slug
- Resolution history (append-only in practice)
- Type classification (Idea vs. Project)

**Dependencies Not Controlled:**
- Review completeness (no enforcement that all ideas receive resolution)
- Resolution quality (HTML field, no structured data)
- Timeline enforcement (no due dates)

**Enforcement Mechanism:**
- Model structure is deliberately minimal
- No workflow enforcement—ideas can remain unresolved indefinitely
- Resolution state inferred from latest Resolve entry

**Boundary Reality:** This domain is intentionally under-constrained. It prioritizes **capture over enforcement**, assuming that organizational pressure handles follow-through. The system makes unresolved ideas visible but does not block anything.

### User & Organizational Structure (`profiles`)
**Responsibility:** Map organizational hierarchy and roles onto Django users.

**Invariants Owned:**
- One profile per user (OneToOne relationship)
- Profile creation automatic via post_save signal
- Notification preferences per user

**Dependencies Not Controlled:**
- Django User model lifecycle
- Correctness of position/site assignments
- Permission logic (delegated to Django/Guardian)

**Enforcement Mechanism:**
- Signal-based automatic profile creation
- No validation that organizational structure is complete
- No enforcement of valid combinations (site + position)

**Boundary Reality:** This is a thin layer over Django auth. The domain models reality but does not validate it. Position and site are user-editable fields, not validated enumerations tied to organizational charts.

### Key Performance Indicators (`kpi`)
**Responsibility:** Track campaign progress against forecasts with automatic rollup.

**Invariants Owned:**
- Campaign uniqueness per year and type: `unique_together = ('year', 'campaign_type')`
- Automatic acumulado calculation on monthly data changes
- Calculated avance (percentage) based on forecast

**Dependencies Not Controlled:**
- Monthly data entry correctness
- Forecast accuracy
- Campaign type consistency across years

**Enforcement Mechanism:**
- Database constraints enforce uniqueness
- Denormalized fields (acumulado, avance) updated via model method
- Editable=False prevents manual tampering with calculated fields

**Boundary Reality:** This domain is tightly constrained. Calculated fields are protected, but the system assumes monthly data is entered correctly. There is no validation that monthly totals align with expected patterns.

## 4. Entity Lifecycles and State Transitions

### Document Lifecycle
**Creation:**
- Manual creation via forms or admin
- Author automatically injected in view/admin save
- Slug auto-generated from nombre
- Initially inactive or in approval state

**Mutation:**
- Document metadata can be updated (nombre, proceso, tipo, flags)
- Revisions are append-only (in practice—no code prevents deletion)
- New Revision triggers checksum calculation automatically
- Notification flags control distribution

**Review Mechanisms:**
- "Report" feature allows external feedback without authentication (with CAPTCHA)
- Reports create tickets with resolution workflow
- Resolution requires authenticated user action

**Terminal States:**
- Documents can be marked inactive (soft delete)
- No concept of "final" or "immutable"—all revisions are theoretically mutable through admin

**Guarding:**
- File integrity protected by checksum
- Checksum_calculado_en and checksum_verificado_en track validation
- No automated integrity checking scheduled—manual verification required

### Action Plan Lifecycle  
**Creation:**
- Manual creation with Plan type selection (CNC or PCM)
- Type determines visible fields (conditional fieldsets in admin)
- User automatically injected on save
- Folio acts as human-readable identifier

**Mutation:**
- Acciones added as children
- Each Accion has assigned responsable and deadlines
- Seguimiento entries appended to track progress
- HTMLField used for rich-text descriptions (introduces XSS risk if not sanitized)

**Review/Approval:**
- No formal approval state machine
- Closure indicated by eliminacion/recurrencia boolean flags
- Status inferred from latest Seguimiento estado field
- CERRADA = 99 is terminal status for Accion

**State Transition Logic:**
- Accion.get_estado() calculates state:
  - "Cerrada" if latest Seguimiento.estado == CERRADA
  - "Abierta Fuera de Tiempo" if fecha_fin < today
  - "Abierta en Tiempo" otherwise
- No validation prevents state regression
- No enforcement of sequential follow-ups

**Archival:**
- No explicit archival mechanism
- Old plans remain accessible indefinitely
- No lifecycle policy (retention, deletion)

### Idea Lifecycle
**Creation:**
- Public form submission (name, contact, site as text—not foreign keys)
- Minimal validation (CAPTCHA likely in production)
- Auto-slug generation

**Resolution:**
- Management adds Resolve entries
- Multiple resolutions allowed (history maintained)
- Latest resolution determines current state (ESPERA, NO_VIABLE, VIABLE)

**Terminal States:**
- No explicit closure
- Ideas never deleted
- Resolution is append-only commentary, not workflow state

**Guarding:**
- No authentication required for submission
- No validation that resolutions are timely
- No enforcement that viable ideas lead to action

## 5. Invariants, Constraints, and Guardrails

### Enforced by Code

**Database-Level:**
- Document-Revision uniqueness ensures no duplicate revision numbers
- Campaign year-type uniqueness prevents duplicate campaigns
- Cascade deletes maintain referential integrity

**Application-Level:**
- Checksum calculation on Revision save
- User auto-injection in admin save hooks
- Profile creation via signals
- Automatic slug generation
- Calculated fields (acumulado, avance) managed by model methods

**Model-Level:**
- Foreign keys enforce entity relationships
- Required fields enforced by blank=False
- Field length limits (CharField max_length)

### Enforced by Convention

**Data Integrity:**
- Revisions are append-only (nothing prevents deletion)
- Status transitions are sequential (nothing enforces order)
- Fechas are meaningful (nothing validates fecha_inicio < fecha_fin)
- Responsible users actually exist (nothing checks User still active)

**Procedural Constraints:**
- All action plans receive analysis (analisis field optional)
- All ideas receive resolution (no deadline enforcement)
- Documents are reviewed before activation (aprobado flag is manual)
- Reports are resolved (resuelto flag, no SLA)

**Organizational Rules:**
- Position assignments match reality (no organizational chart validation)
- Site assignments are correct (no lookup table)
- Email addresses are valid (Django validates format only)

### Audit Requirements

**Traceability Maintained:**
- Created/updated timestamps on all core entities
- Author/user tracking via foreign keys
- Revision history preserved
- Notification history logged

**Gaps:**
- No audit log of who changed what fields
- No django-simple-history integration (despite requirements.txt inclusion)
- No change approval workflow
- No rollback mechanism

### What Is Not Constrained

**Deliberate Flexibility:**
- Text fields for descriptions (allows rich context, prevents structure)
- HTMLField usage (enables formatting, introduces XSS risk)
- Optional evidence uploads (documents intent, doesn't enforce proof)
- Soft state machines (observable status, not enforceable transitions)

**Intentional Gaps:**
- No permission system observed (LoginRequiredMixin used, but not granular)
- No workflow automation (reminders, escalations)
- No data validation rules (business logic in forms, not models)

## 6. Ownership Posture Embedded in the System

### High-Risk Change Zones

**Schema Migrations:**
- Document-Revision relationship changes risk orphaning files
- Changing unique_together could allow duplicate revisions
- CASCADE deletes mean parent deletion is irreversible
- No soft-delete pattern—deletion is permanent

**File Handling:**
- Checksum calculation in save() means file operations must complete
- Changing upload_to functions risks breaking existing file paths
- Archivo field changes could orphan physical files

**Calculated Fields:**
- Modifying acumulado/avance logic requires historical recalculation
- Changing estado calculation affects all historical interpretations

### Where Mistakes Have Long-Lived Consequences

**Data Model Changes:**
- Revision history is permanent record—cannot be "fixed" without explanation
- User assignments become part of audit trail
- Timestamps are immutable once written

**Process Logic:**
- Status calculation changes affect how historical plans are interpreted
- Changing what constitutes "closed" reinterprets all past closures

### Where Code Expects Human Judgment

**Resolution Quality:**
- System records resolutions but doesn't validate them
- Viability determination is entirely human
- Closure adequacy not programmatically assessed

**Evidence Sufficiency:**
- File uploads optional—human decides if evidence is adequate
- Analysis depth not validated—text field accepts any content

**Responsibility Assignment:**
- System allows any user assignment—humans must assign appropriately
- No validation that assigned user has capacity or authority

### Where to Slow Down Deliberately

**Before Migration:**
- Any change to Revision model
- Any change to unique constraints
- Any CASCADE delete introduction

**Before Changing:**
- Estado/status calculation logic
- Checksum algorithms (breaks historical verification)
- File upload paths (breaks file resolution)

**Before Removing:**
- Any field that might exist in production data
- Any model with foreign key references
- Any historical tracking field

## 7. Decision-Making Signals

### Safe to Extend

**New Reports/Views:**
- Adding read-only views is low-risk
- New reporting queries safe if read-only
- New export formats straightforward

**New Features:**
- Additional flags on existing models (nullable, with defaults)
- New apps following existing patterns
- New notification types

**UI/Template Changes:**
- Template modifications isolated from data model
- Form field additions (if nullable)
- CSS/JavaScript changes

### Fragile/Irreversible

**Data Model Changes:**
- Removing fields (data loss)
- Changing uniqueness constraints (migration complexity)
- Renaming models (foreign key updates)
- Changing CASCADE behavior (implicit deletions)

**File Operations:**
- Changing upload_to paths (breaks existing references)
- Modifying checksum algorithm (invalidates historical checksums)

**Calculated Logic:**
- Changing status inference
- Modifying aggregation calculations
- Altering date-based computations

### Constraining Couplings

**Direct Database References:**
- All apps share database—schema changes cascade
- No API versioning—all clients see changes immediately
- Foreign keys couple lifecycles

**Shared User Model:**
- All domains reference Django User
- Profile changes affect all apps
- Authentication changes global

**File System Coupling:**
- MEDIA_ROOT path changes affect all uploads
- File naming conventions shared
- Backup strategies must handle files + DB atomically

### Visible Technical Debt

**Intentional:**
- HTMLField for rich text (risk accepted for usability)
- Manual user injection (avoiding complex auth logic)
- Soft state machines (flexibility over enforcement)
- Optional evidence fields (pragmatism over rigor)

**Accidental:**
- django-simple-history in requirements but not used
- watson search integrated but coverage unclear
- guardian installed but permissions not comprehensively applied
- Multiple unused fields (aprobado flag, ruta URL field)

## 8. Operational and Scale Implications

### Data Longevity
This system is designed for **permanent retention**. Revisions accumulate indefinitely. Action plans remain accessible forever. Ideas are never purged. There is no archival strategy, no retention policy, no deletion workflow.

**Implications:**
- Storage grows monotonically
- Query performance degrades over time without indexing strategy
- Reporting must filter by date ranges explicitly
- Backup sizes grow continuously

### Auditability Characteristics

**Strong Traceability:**
- Who created what when (author + timestamps)
- Document revision history complete
- Action plan follow-up sequence preserved
- Notification delivery logged

**Weak Traceability:**
- No field-level change tracking (despite simple-history in dependencies)
- No approval audit trail
- No record of who viewed what
- No access logs

**Sensitivity to Incorrect Mutations:**
- Manual revision deletion destroys history (no soft delete)
- Incorrect status updates misrepresent reality permanently
- Bad fecha data corrupts temporal reasoning
- Wrong responsibility assignments become false audit trail

### Operational Burden

**Maintenance Requirements:**
- Checksum verification must be scheduled externally
- File system integrity not monitored
- Dead files not cleaned (if records deleted)
- No automated data quality checks

**Deployment Complexity:**
- Migrations must run before code deploys (standard Django)
- Static file collection required
- Media files must persist across deploys
- Database backup must be consistent with file system

**Standardization Suitability:**
- System hardcoded to single organization (TLAXCALA constant)
- Site enumeration hardcoded (Junta Local, Distrital)
- Position codes specific to Mexican electoral organization (VEL, VOL, etc.)
- No multi-tenancy support

**This is a single-organization system.** Adapting it for another organization requires code changes, not configuration.

## 9. What This Reveals About Engineering Judgment

### Values Encoded

**Stability Over Agility:**
- Django LTS patterns, not cutting-edge features
- Direct database coupling over service architecture
- Minimal abstractions, maximum clarity
- Evolution through addition, not refactoring

**Traceability Over Efficiency:**
- Redundant author fields on every entity
- Denormalized calculations for query performance
- Explicit timestamps everywhere
- Preservation of history even when awkward

**Human Judgment Over Automation:**
- Workflow suggestions, not enforcement
- Status inference, not state machines
- Optional evidence, not mandatory proof
- Soft deadlines, not hard gates

**Operational Continuity Over Modularity:**
- Tight coupling accepted for simplicity
- Shared database reduces coordination
- No service boundaries to version or maintain
- Single deploy, single failure domain

### Trade-Offs Prioritized

**Accepted:**
- Tight coupling for operational simplicity
- Manual processes for flexibility
- HTMLField XSS risk for rich content
- Soft state machines for adaptability

**Avoided:**
- Distributed systems complexity
- Strict workflow enforcement
- Granular permission systems
- Automated testing infrastructure (no tests observed)

### Cultural Alignment

This system reflects an engineering culture that:
- **Values institutional memory** (permanent records, full history)
- **Trusts human judgment** (soft constraints, optional evidence)
- **Prioritizes reliability** (boring technology, proven patterns)
- **Accepts resource constraints** (pragmatic shortcuts, manual processes)
- **Operates under regulatory pressure** (audit trails, traceability)
- **Expects long system lifespan** (extensibility through addition)

The system is not trying to be innovative. It is trying to be **dependable, traceable, and maintainable by a small team over many years.**

This is governance infrastructure built for stability, not velocity. The engineering posture required is one of **deliberate evolution**, where changes are additive, migrations are carefully planned, and breaking changes are avoided because the cost of disruption exceeds the benefit of modernization.

The system will not fail from technical debt. It will fail if organizational procedures outgrow the flexibility of soft constraints, or if data volume overwhelms query performance, or if the maintainer who understands the implicit conventions leaves without documentation.

**The primary risk is not code quality—it is knowledge transfer.**

---

## Conclusion

Cerebro is a system that makes organizational accountability executable. It succeeds by being boring, explicit, and permanent. It demands engineering discipline not in sophisticated abstractions but in careful stewardship of irreversible records and long-lived data.

The ownership posture this system demands is **conservative by design**. Changes should be additive. History should be preserved. Constraints should be loosened carefully. The system protects institutional memory at the cost of architectural elegance.

This is appropriate.
