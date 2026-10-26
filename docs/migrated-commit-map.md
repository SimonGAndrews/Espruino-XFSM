# XFSM Migrated Commit Map

Early XFSM development took place under `libs/xfsm/` in the
[`SimonGAndrews/Espruino`](https://github.com/SimonGAndrews/Espruino)
repository. That path's history was later extracted into the standalone
[`SimonGAndrews/Espruino-XFSM`](https://github.com/SimonGAndrews/Espruino-XFSM)
repository.

The extraction retained the XFSM changes and commit details, but Git assigned
new commit hashes because the surrounding repository history changed. Use this
table to translate an Espruino commit cited by an older test result or report
into the corresponding standalone XFSM commit.

The map covers all 35 extracted commits. Each pair has the same author, date,
and subject, and the final extracted tree has the same Git tree hash as the
original `libs/xfsm/` directory: `b774d877e4284eaf5fae8ae1b7a5366512364c53`.
An original Espruino commit may also contain changes outside `libs/xfsm/`; its
standalone partner contains only the extracted XFSM history.

| Original Espruino commit | Standalone XFSM commit | Date | Subject |
| --- | --- | --- | --- |
| [`225e55fba3`](https://github.com/SimonGAndrews/Espruino/commit/225e55fba32b7a859a30ae5ba5db0c8e4f9f4ff6) | [`dbdf6bca88`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/dbdf6bca881580198b9a57ddbe1585a9a4870443) | 2026-09-25 | Add XFSM optional library shell |
| [`d4860d07a9`](https://github.com/SimonGAndrews/Espruino/commit/d4860d07a93a725176f6216321b3d47f2d0a14cf) | [`54cf405ce7`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/54cf405ce74145342ca02a27bdb6472c2e17d1c3) | 2026-09-25 | Add XFSM native format foundation |
| [`80d424772d`](https://github.com/SimonGAndrews/Espruino/commit/80d424772d08bbeb713288b1b1cad5b262cdfe9a) | [`bac9662bee`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/bac9662beeafed6734558c5aafb097ccb7b59fda) | 2026-09-25 | Implement XFSM machine construction slice |
| [`c6505437ad`](https://github.com/SimonGAndrews/Espruino/commit/c6505437ad630c1fc715662d9bc5050737dd67f0) | [`fe17871b8e`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/fe17871b8e932b5969f82fcf8d00ce7bad3f56bc) | 2026-09-25 | Implement XFSM M4 actor runtime |
| [`de251bd977`](https://github.com/SimonGAndrews/Espruino/commit/de251bd977cc5b6bdccd83f72b872a0911fd6866) | [`f4252587de`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/f4252587decb2e97b66622cb601c283523c36374) | 2026-09-25 | Add XFSM M5 resource instrumentation |
| [`8794dc1d78`](https://github.com/SimonGAndrews/Espruino/commit/8794dc1d789f87cb57fcb6b460ef1d89c3f5bc06) | [`5b9b846f56`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/5b9b846f565f7fbdd205f40a48581c7c07e5ec55) | 2026-09-25 | Add XFSM development CI |
| [`4d4ef00b90`](https://github.com/SimonGAndrews/Espruino/commit/4d4ef00b904e33618d2c75cf427d1d9af4b3292b) | [`e174c772ae`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/e174c772aede1a42cf3a05be1dc104bf6f702605) | 2026-09-25 | Add ESP32 M5 measurement harness |
| [`e5c9dde04d`](https://github.com/SimonGAndrews/Espruino/commit/e5c9dde04d32d3c89bba2ce6ae4ec552b9a6292d) | [`155084cd63`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/155084cd63cfd97b84f3c8c57893ca69293f5793) | 2026-09-27 | Implement XFSM completion and M6 behavior |
| [`69a32ab303`](https://github.com/SimonGAndrews/Espruino/commit/69a32ab303b09b140522c382f3c45329ace449ee) | [`46402c5652`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/46402c565214168b36046b3a9815a09caeafb90b) | 2026-09-27 | Expand XFSM development coverage |
| [`4d0e5b504a`](https://github.com/SimonGAndrews/Espruino/commit/4d0e5b504a1b1d99eb8c938012e8e8a0bf8f8355) | [`cb3734bbd3`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/cb3734bbd39e2345ebbd4a725a059ad210ea7aa5) | 2026-09-27 | Document XFSM usage and test workflows |
| [`c91f441a83`](https://github.com/SimonGAndrews/Espruino/commit/c91f441a83f54872fe781cc1169226d061e8ebb9) | [`2568d66239`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/2568d662397612070ff9a47a680dd1b97f3608f4) | 2026-09-27 | Complete XFSM transition-domain traversal |
| [`2b31e01c0a`](https://github.com/SimonGAndrews/Espruino/commit/2b31e01c0a436257a60b4e755b111cd040e5ce8c) | [`6e4390730f`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/6e4390730f45f9d3265f604908a624f3a48fe93c) | 2026-09-27 | Complete XFSM lifecycle and host integration coverage |
| [`319adfef5d`](https://github.com/SimonGAndrews/Espruino/commit/319adfef5d74890deedc11ce140bb32ca5e0fce1) | [`e6bd4a65b1`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/e6bd4a65b11bc4f728a636bcba5bd48484656c8a) | 2026-09-27 | Complete XFSM validation and allocation failure handling |
| [`1589218d30`](https://github.com/SimonGAndrews/Espruino/commit/1589218d30bcd761d1e323cd09b93187417a4797) | [`f9362a7f06`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/f9362a7f0628bcbaa499125d64488d2de3f467f2) | 2026-09-27 | Measure complete XFSM resource use |
| [`21154897f3`](https://github.com/SimonGAndrews/Espruino/commit/21154897f3c5a76864989ade0c5ac959e35bd8f7) | [`f37d020758`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/f37d020758af84b3c4d208a3a5929af08e2fd629) | 2026-09-27 | Test XFSM physical application integration |
| [`b7b6d88d79`](https://github.com/SimonGAndrews/Espruino/commit/b7b6d88d79ab8602574f1551804bd1baa672f96f) | [`aa6fa1003f`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/aa6fa1003fb4c317bb46f2a7e713595644ecabf4) | 2026-09-27 | Test XFSM memory cleanup and event serialization |
| [`8ce408fb56`](https://github.com/SimonGAndrews/Espruino/commit/8ce408fb560ed60b33d327f2feb7fac856e3f8ac) | [`92282a66f6`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/92282a66f6b4994f3082b2c51c12a5f68286dce6) | 2026-09-27 | Harden XFSM allocation diagnostics |
| [`cb5d74e895`](https://github.com/SimonGAndrews/Espruino/commit/cb5d74e8953ac7b4290aaba64f2aabe7714a3a05) | [`5545175cba`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/5545175cbac4d9c0220aefbae90e4721c461e67f) | 2026-09-27 | Reduce XFSM compiler JsVar peak |
| [`aded959ada`](https://github.com/SimonGAndrews/Espruino/commit/aded959ada37449c59b4a79e67133cd4cc4cbd2b) | [`21b0b9a43c`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/21b0b9a43ce958e162e6f50aaf05d113d34d35ee) | 2026-09-28 | Test XFSM wireless service coexistence |
| [`c25a1c32dd`](https://github.com/SimonGAndrews/Espruino/commit/c25a1c32dd07369e8a7ec42d6c853ada641019d6) | [`cc4b31482d`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/cc4b31482d13b0da3b2c47728188509ca0e37b65) | 2026-09-28 | Add embedded XFSM fault qualification |
| [`9b813aa304`](https://github.com/SimonGAndrews/Espruino/commit/9b813aa304407652828221e243acc51d81e5240a) | [`d55eebe200`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/d55eebe2001ff6d152f456cdb3dbe7550ef1ad4d) | 2026-09-28 | Close XFSM public and configuration cases |
| [`ba0f275334`](https://github.com/SimonGAndrews/Espruino/commit/ba0f275334a9f30a007bda27fa62a40073e2aa18) | [`5666b4ddfb`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/5666b4ddfb93346ee7df888a2f8473ddac159245) | 2026-09-28 | Close XFSM runtime contract cases |
| [`02c8a054fe`](https://github.com/SimonGAndrews/Espruino/commit/02c8a054feea4999f21c477978bc46637b4b645e) | [`ff22c8a6a3`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/ff22c8a6a3e8e290fc538521836c7b02615cefb2) | 2026-09-28 | Close XFSM structural contract cases |
| [`6ed09d5d24`](https://github.com/SimonGAndrews/Espruino/commit/6ed09d5d2444f5355e1573bcbd46094c362c6edf) | [`27d85b4806`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/27d85b480688119190079ae3ee3b8575f0434c4a) | 2026-09-29 | Add XFSM compatibility differential traces |
| [`e772a1d447`](https://github.com/SimonGAndrews/Espruino/commit/e772a1d44701e1f3709105b989de9ce2fde61227) | [`59e3ca9209`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/59e3ca92099c5f21f8ad4b156a56caf3b50b37b9) | 2026-09-29 | Make physical XFSM fixtures target-portable |
| [`190d14a904`](https://github.com/SimonGAndrews/Espruino/commit/190d14a9042847870010f5c08868e6908f09f251) | [`e7da509f1e`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/e7da509f1ecca44f6edbc78dad6aecfb83f16ab0) | 2026-09-29 | Make constrained-target fixtures portable |
| [`48d8d3e8e0`](https://github.com/SimonGAndrews/Espruino/commit/48d8d3e8e0d32885188a40dd319d7e90b9e9b86a) | [`a88e1c47fc`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/a88e1c47fcca533eadbd4f0407a7e0ca0965525c) | 2026-10-01 | Document XFSM implementation structure |
| [`3b3952b9cd`](https://github.com/SimonGAndrews/Espruino/commit/3b3952b9cd2c1d46e4aeab3ed1b076b8d4bcc8d0) | [`27c039bf30`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/27c039bf30d9baf52d5d9833bd1d72a1ec3ee1da) | 2026-10-20 | Add experimental shallow history support |
| [`007d8b4b44`](https://github.com/SimonGAndrews/Espruino/commit/007d8b4b441f0729f19d41e30548b7f044ac9a89) | [`d28386aefe`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/d28386aefe5d9a2b0d62946bed36a997aceafefb) | 2026-10-21 | Add experimental deep history support |
| [`4a0d53f997`](https://github.com/SimonGAndrews/Espruino/commit/4a0d53f997a856d66fb4799b1bd1c5b5228afb51) | [`340d5d9dea`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/340d5d9deabeb26ac606617362968b9bc20c32d0) | 2026-10-21 | Document XFSM history implementation flow |
| [`5a044617a2`](https://github.com/SimonGAndrews/Espruino/commit/5a044617a239d2ea9653ebc7b214ba0e67fda25b) | [`27d11646b9`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/27d11646b9883980ff97ef06cffce913293291c9) | 2026-10-21 | Reduce XFSM compiler history metadata |
| [`4508ea9a0b`](https://github.com/SimonGAndrews/Espruino/commit/4508ea9a0b910961fcc3bdf59f3fdce48a927d5e) | [`6c9904b207`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/6c9904b2078b574b349f61aaeba058dbd5fa71a2) | 2026-10-21 | Prepare XFSM history banks lazily |
| [`6f42145347`](https://github.com/SimonGAndrews/Espruino/commit/6f42145347d8f4018b2a1ec221b3834bf9561a24) | [`cd31b50e85`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/cd31b50e85104a6e063f84eeff4de6092596f134) | 2026-10-21 | Align XFSM history transaction comments |
| [`83d2691db8`](https://github.com/SimonGAndrews/Espruino/commit/83d2691db8ea15e63912bdbfff028e9d13666f86) | [`b3220f9c9a`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/b3220f9c9ad7cb021d4998c0c45879b1a9466423) | 2026-10-21 | Promote XFSM to Profile 2 |
| [`55f45513f1`](https://github.com/SimonGAndrews/Espruino/commit/55f45513f1e0024bd032d4bcc506c3573067fc57) | [`ad07e56f7e`](https://github.com/SimonGAndrews/Espruino-XFSM/commit/ad07e56f7ec2550d7afe483f10fa0a4c24643bc8) | 2026-10-22 | Adapt XFSM to current string comparison API |

Commits after `ad07e56f7e` were made directly in the standalone repository and
therefore do not require migration mapping. New Espruino integration commits
record their standalone source with an `XFSM-Source: <commit>` reference line.
