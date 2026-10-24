# Taazour Aoun

Taazour Aoun connects beneficiary eligibility, identity verification and a wallet-transfer journey. Several independent checks become one understandable sequence: establish eligibility, complete the appropriate identity step, select a destination and inspect the transfer outcome.

The journey needs to work in Arabic with right-to-left layout while retaining French and English. External identity, eligibility, messaging and payment systems also have different contracts and failure conditions; completing a screen cannot stand in for a confirmed payment.

Three mechanisms structure the application:

- An explicit step flow separates eligibility, OTP or electronic identity verification, wallet choice and transfer confirmation. The interface can present the next required action instead of hiding the process inside a single long form.
- Server-side actions call an integration boundary that keeps external service contracts out of the presentation layer. Mock implementations make the journey testable while partner connections are developed.
- The wallet step distinguishes selecting an owned wallet from supplying destination details for another wallet. Identity verification, destination selection and payment confirmation remain separate concerns.

The beneficiary journey currently runs against mocked external integrations; live partner connections remain separate integration work.

Developed within IBTIKAR Technologies’ engineering team across application and integration work.

**Technology:** Next.js, React, TypeScript, multilingual routing and server-side validation.

**Code: private**

---

[← Back to the observatory](../README.md#user-content-systems)
