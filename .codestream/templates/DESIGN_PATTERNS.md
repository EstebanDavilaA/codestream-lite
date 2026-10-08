# Design Patterns & Architectural Archetypes

Reference material for `/plan`, `/execute` and the reviewer in `/steer`. Not
process, not ceremony.

A pattern earns its place in a slice only when it prevents a real problem —
testability, regression risk, combinatorial explosion. Naming it is not enough:

1. **The spec names it**, in *Rules and patterns that apply*, along with the
   boundary it draws and the shape it forbids — e.g. "port/adapter —
   `DESIGN_PATTERNS#2`; `subprocess` may only be imported inside the adapter
   class."
2. **At least one item in *How we will know it works* can fail** if the boundary
   is crossed. A pattern nobody can check is a comment.
3. **The build honours the contract**, with no shortcuts: no adapter bypassed by
   direct I/O, no strategy collapsed into an inline `if/else` ladder.
4. **The reviewer looks at the boundary specifically** (rule 5), because a pattern
   is exactly the kind of thing that reads correctly in a summary and isn't in
   the code.

---

## Core Pattern Archetypes

### 1. Strategy / Policy (Polymorphic Dispatch)

- **Literature Precedent:** GoF (*Behavioral*, p. 268); Fowler (*Refactoring: Replace Conditional with Polymorphism*).
- **Target Smell / Anti-Pattern:**
  - Combinatorial `switch` / `if-else` ladders switching on types, roles, or operational modes.
  - Adding a new variant requires modifying existing core business methods and risks breaking existing variants.
- **Core Abstraction:**
  - Define a common execution interface/signature: `execute(context: Context) -> Result`.
  - Encapsulate each algorithm variant in an independent strategy implementation (class, pure function, or module).
  - Context receives or selects the strategy dynamically or via configuration.
- **Spec Norm Declaration Example:**
  > `Norm: Pricing algorithms must implement the PricingStrategy interface. SalesOrder delegates calculation to the installed strategy; no inline branching on customer tier in order calculation. Precedent: .codestream/templates/DESIGN_PATTERNS.md#strategy`
- **Acceptance Criteria Archetype:**
  | ID | Requirement | Test Type | Expected Outcome |
  |:---|:---|:---|:---|
  | AC-STRAT-1 | Strategy Isolation | `Unit Test` | Each strategy variant tested in isolation with deterministic inputs/outputs |
  | AC-STRAT-2 | Open-Closed Boundary | `Structure` | Adding a mock strategy variant executes cleanly through caller without editing caller code |
- **Critic Audit Gate:**
  - Check that the caller contains zero `if (type == ...)` switching on strategy variants.

---

### 2. Port & Adapter (Hexagonal / Clean Architecture)

- **Literature Precedent:** Cockburn (*Hexagonal Architecture*); Martin (*Clean Architecture*); GoF (*Adapter*, p. 78).
- **Target Smell / Anti-Pattern:**
  - Core domain logic directly imports or instantiates database clients, network SDKs, third-party APIs, or OS file handles.
  - Business rules cannot be tested without spinning up full databases or live network connections, or relying on fragile monkey-patching.
- **Core Abstraction:**
  - **Port:** An abstract interface owned by the domain defining what the domain needs (e.g. `UserRepository`, `PaymentGateway`).
  - **Adapter:** An infrastructure implementation wrapping the concrete external service (e.g. `PostgresUserRepository`, `StripePaymentGateway`).
- **Spec Norm Declaration Example:**
  > `Norm: Domain services must interact with storage solely through the UserRepository port interface. Zero direct database imports in domain/services. Precedent: .codestream/templates/DESIGN_PATTERNS.md#port-adapter`
- **Acceptance Criteria Archetype:**
  | ID | Requirement | Test Type | Expected Outcome |
  |:---|:---|:---|:---|
  | AC-PORT-1 | Mock Isolation | `Unit Test` | Domain service unit tests execute 100% against in-memory mock adapter with 0 I/O calls |
  | AC-PORT-2 | Dependency Direction | `Structure` / `Lint` | Static import scan confirms domain package has zero dependencies on infrastructure/database drivers |
- **Critic Audit Gate:**
  - Trace all imports in domain modules; reject any direct instantiation of concrete infrastructure classes.

---

### 3. State Machine (Explicit Finite State Transitions)

- **Literature Precedent:** GoF (*State*, p. 255); Fowler (*State Pattern*).
- **Target Smell / Anti-Pattern:**
  - Boolean flag explosion (`isLoading`, `isPending`, `hasFailed`, `isRetrying`, `canCancel`) where invalid state combinations occur (e.g. `isLoading && hasFailed`).
  - Transition rules scattered across multiple handlers and event callbacks.
- **Core Abstraction:**
  - Explicit finite set of states (enum, sealed types, or state objects).
  - Explicit transition matrix: `transition(current_state, event) -> next_state`.
  - Illegal transitions fail fast and explicitly rather than silently corrupting state.
- **Spec Norm Declaration Example:**
  > `Norm: Order lifecycle managed via explicit State Machine. State transitions must be validated against the transition table; direct mutation of state string/flag is prohibited. Precedent: .codestream/templates/DESIGN_PATTERNS.md#state-machine`
- **Acceptance Criteria Archetype:**
  | ID | Requirement | Test Type | Expected Outcome |
  |:---|:---|:---|:---|
  | AC-STATE-1 | Valid Transitions | `Unit Test` | Defined event sequences transition from State A to State B as specified |
  | AC-STATE-2 | Illegal Transition Guard | `Unit Test` | Triggering invalid transition (e.g. Cancelled -> Shipped) throws InvalidStateTransitionError |
- **Critic Audit Gate:**
  - Verify that state transitions are centralized and cannot be bypassed by external callers modifying raw fields.

---

### 4. Dependency Inversion & Injection (DI)

- **Literature Precedent:** Martin (*DIP - Dependency Inversion Principle*); Fowler (*Inversion of Control Containers and the Dependency Injection Pattern*); GoF Update (p. 319).
- **Target Smell / Anti-Pattern:**
  - Hardcoded `new Service()` instantiation inside consumer constructors or methods.
  - Use of global mutable singletons that prevent concurrent execution or isolated unit tests.
- **Core Abstraction:**
  - Higher-level modules depend on abstractions, not concretions.
  - Dependencies are injected via constructor or function parameters, rather than fetched internally.
- **Spec Norm Declaration Example:**
  > `Norm: Constructor injection only for all service dependencies. Singletons and global registry lookups prohibited. Precedent: .codestream/templates/DESIGN_PATTERNS.md#dependency-injection`
- **Acceptance Criteria Archetype:**
  | ID | Requirement | Test Type | Expected Outcome |
  |:---|:---|:---|:---|
  | AC-DI-1 | Constructor Injection | `Structure` | Service accepts port interfaces via constructor parameters; no global singleton lookups |
  | AC-DI-2 | Isolated Instantiation | `Unit Test` | Service can be instantiated and tested with custom mock dependencies without global setup |
- **Critic Audit Gate:**
  - Check for static accessor calls (e.g. `ServiceLocator.get()` or global imports of singleton instances) inside class bodies.

---

### 5. Factory / Creation Method

- **Literature Precedent:** GoF (*Abstract Factory*, p. 12; *Factory Method*, p. 40); Bloch (*Effective Java, Item 1: Static factory methods*).
- **Target Smell / Anti-Pattern:**
  - Complex construction logic (parameter validation, sub-object assembly, caching) duplicated across multiple client call sites.
  - Clients tightly coupled to concrete constructors whose signatures change frequently.
- **Core Abstraction:**
  - Separate object creation from object utilization.
  - Creation function or factory object returns the interface/abstract type.
- **Spec Norm Declaration Example:**
  > `Norm: Complex entity construction must use dedicated static creation methods with descriptive intent names. No public multi-argument constructors with ambiguous primitive types. Precedent: .codestream/templates/DESIGN_PATTERNS.md#factory`
- **Acceptance Criteria Archetype:**
  | ID | Requirement | Test Type | Expected Outcome |
  |:---|:---|:---|:---|
  | AC-FACT-1 | Factory Construction | `Unit Test` | Factory method validates input invariant and returns fully configured interface instance |
  | AC-FACT-2 | Construction Decoupling | `Structure` | Caller code invokes creation method without referencing concrete subclass names |
- **Critic Audit Gate:**
  - Ensure client code references the factory and abstract return interface, not concrete constructor internals.

---

### 6. Observer / Pub-Sub / Event Dispatcher

- **Literature Precedent:** GoF (*Observer*, p. 237).
- **Target Smell / Anti-Pattern:**
  - A primary domain event (e.g. `UserRegistered`) triggers direct, synchronous calls to an ever-growing list of secondary tasks (send welcome email, create analytics record, update search index, provision defaults) tightly coupling the core flow to side-effects.
- **Core Abstraction:**
  - Publisher emits an immutable event payload to a dispatcher or subscriber registry.
  - Subscribers handle the event independently; publisher remains unaware of subscriber count or identities.
- **Spec Norm Declaration Example:**
  > `Norm: Domain state modifications emit domain events to EventDispatcher. Side-effect processors (email, telemetry) subscribe independently; core domain method does not call notification services directly. Precedent: .codestream/templates/DESIGN_PATTERNS.md#observer`
- **Acceptance Criteria Archetype:**
  | ID | Requirement | Test Type | Expected Outcome |
  |:---|:---|:---|:---|
  | AC-OBS-1 | Event Emission | `Unit Test` | Executing domain action emits typed DomainEvent with expected payload |
  | AC-OBS-2 | Subscriber Independence | `Integration Test` | Disabling or adding a subscriber does not alter domain action return value or execution flow |
- **Critic Audit Gate:**
  - Check that the subject class does not hold direct references to downstream notification/analytics classes.

---

### 7. Pipeline / Middleware / Interceptor

- **Literature Precedent:** Buschmann et al. (*POSA Patterns of Software Architecture: Pipes and Filters*); GoF (*Chain of Responsibility*, p. 160).
- **Target Smell / Anti-Pattern:**
  - Monolithic handler function performing parsing, validation, authentication, rate limiting, domain execution, and error formatting in one giant block.
- **Core Abstraction:**
  - Discrete, composable processing stages sharing a standard step contract: `handle(request, next) -> response`.
  - Stages can be reordered, added, or tested in complete isolation.
- **Spec Norm Declaration Example:**
  > `Norm: Inbound request processing structured as a composable middleware pipeline. Authentication and rate-limiting are isolated pipeline steps, not embedded in route handler logic. Precedent: .codestream/templates/DESIGN_PATTERNS.md#pipeline`
- **Acceptance Criteria Archetype:**
  | ID | Requirement | Test Type | Expected Outcome |
  |:---|:---|:---|:---|
  | AC-PIPE-1 | Stage Isolation | `Unit Test` | Each middleware filter tested independently with stubbed next-delegate |
  | AC-PIPE-2 | Pipeline Short-Circuit | `Unit Test` | Failure in early stage (e.g. Auth) halts pipeline and prevents invocation of downstream stages |
- **Critic Audit Gate:**
  - Verify that each stage handles exactly one concern and delegates cleanly to the next handler.

---

### 8. Composite (Uniform Part-Whole Hierarchy)

- **Literature Precedent:** GoF (*Composite*, p. 100).
- **Target Smell / Anti-Pattern:**
  - Code contains distinct recursive branches for "single element" vs "container of elements" (e.g. file vs folder, single task vs composite task).
- **Core Abstraction:**
  - A common interface represents both individual leaves and containers of leaves.
  - Clients treat single components and composite structures uniformly without `instanceof` / type checking.
- **Spec Norm Declaration Example:**
  > `Norm: Menu items and submenus must implement the MenuItemComponent interface. Rendering and permission checks operate uniformly across leaf items and composite submenus without type branches. Precedent: .codestream/templates/DESIGN_PATTERNS.md#composite`
- **Acceptance Criteria Archetype:**
  | ID | Requirement | Test Type | Expected Outcome |
  |:---|:---|:---|:---|
  | AC-COMP-1 | Uniform Traversal | `Unit Test` | Invoking operation on root composite recursively aggregates results across all children |
  | AC-COMP-2 | Leaf/Composite Uniformity | `Structure` | Client renderer calls interface method uniformly with zero runtime type-casting (`instanceof`) |
- **Critic Audit Gate:**
  - Scan caller code for `instanceof` or type tags differentiating leaves from containers.

---

## The YAGNI Guardrail

> [!WARNING]
> **Do not add patterns where simpler, straightforward code suffices.**
> Design patterns exist to prevent tangible friction (testability failure, regression risk, combinatorial explosion).
> - If a function has 2 stable options that never change, a simple boolean or ternary is correct — do not build a `StrategyFactory`.
> - If code does not need mock substitution or external isolation, direct calls are correct — do not build an `Adapter` layer for internal utilities.
> - A genuinely small change (rule 2's exception) skips pattern extraction entirely. Make the change, keep it minimal, and say what you did.

