import { evaluateHousehold, prepareApplicationPacket, validateApplicationPacket } from '../lib/benefits.mjs';
import { prepareLocalApplicationPacket, validateLocalApplicationPacket } from '../public/packet-core.js';

const household = {
  adults: 1,
  singleParent: true,
  children: [{ age: 7 }, { age: 12 }],
  monthlyGrossIncome: 2000,
  warmRent: 1100,
  receivesKindergeld: true,
  city: 'Berlin'
};
const details = {
  applicant_name: 'Mara Beispiel',
  applicant_address: 'Sonnenallee 100, 12045 Berlin',
  applicant_email: 'mara@example.invalid',
  basic_security_status: 'No (self-attested)'
};
const preparedEvidence = ['income_proof', 'housing_proof'];

const result = evaluateHousehold(household);
if (!result.ok) throw new Error('Smoke household failed');
if (result.summary.knownMonthly !== 518) throw new Error(`Expected €518 known, got ${result.summary.knownMonthly}`);
if (result.summary.potentialAdditionalMax !== 594) throw new Error(`Expected €594 KiZ max, got ${result.summary.potentialAdditionalMax}`);

const serverPacket = prepareApplicationPacket(result, 'kiz', { applicationDetails: details, preparedEvidence });
const localPacket = prepareLocalApplicationPacket(result, 'kiz', { applicationDetails: details, preparedEvidence });
if (serverPacket.status !== 'ready_for_human_review') throw new Error('Server packet not ready for human review');
if (localPacket.status !== 'ready_for_human_review') throw new Error('Local packet not ready for human review');

const review = { claims_reviewed: true, evidence_status_reviewed: true, not_submission_understood: true };
const serverValidation = validateApplicationPacket(serverPacket, review);
const localValidation = validateLocalApplicationPacket(localPacket, review);
if (!serverValidation.readyForOfficialServiceHandoff || !localValidation.readyForOfficialServiceHandoff) throw new Error('Reviewed packet not ready for handoff');
if (serverValidation.submissionAllowed || localValidation.submissionAllowed) throw new Error('Submission boundary violated');

console.log(JSON.stringify({
  ok: true,
  headline: result.summary.headline,
  traceId: result.traceId,
  serverPacketId: serverPacket.packetId,
  localPacketId: localPacket.packetId,
  packetStatus: localPacket.status,
  submissionAllowed: false
}, null, 2));
