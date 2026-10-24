# Taazour Pay

Taazour Pay develops the cash-transfer workflow into a configurable payment application. It connects household eligibility, identity verification, wallet selection and beneficiary confirmation while allowing different providers behind the same user journey.

Eligibility belongs to a household, so different eligible holders must not create independent successful payments for one entitlement. Provider interactions can also be asynchronous: an account or transfer request may need confirmation before the application can present a final outcome.

Three mechanisms address those constraints:

- A durable household payment lock places duplicate control in persistent application state, rather than relying on a disabled browser button. The same household boundary applies across payment backends.
- A provider adapter separates the beneficiary workflow from the external payment implementation. Provider changes do not require duplicating eligibility, identity and confirmation logic throughout the interface.
- The server binds beneficiary and amount context while the interface asks the person to confirm returned destination details. Requesting an operation and receiving its confirmed result are treated as different steps.

Direct-provider adapters are mocked while integrations are developed; other partner connections require activation separately from application deployment.

Developed collaboratively within IBTIKAR Technologies’ engineering team.

**Technology:** Next.js, React, TypeScript, MongoDB/Mongoose, Redis and BullMQ.

**Code: private**

---

[← Back to the observatory](../README.md#user-content-systems)
