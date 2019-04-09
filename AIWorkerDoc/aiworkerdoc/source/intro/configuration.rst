Configuration
=============


**Example**

    .. code-block:: json

        {
              "ledger": "http://54.211.127.67:8080",
              "node": "http://18.215.32.172:8051",
              "wallet": "0xeF980D9ACB9Bd396b38b0A0A5de834d70A9b9125",
              "price_limit": "1",
              "dual_mode": true
        }

    ``ledger`` and "node" are on your choice. You can choose you preferred service
    provider or use the default we provided. Check `Nebula Orion Cloud Platform <https://nbai.io/>`_
    for all available official choices.

    ``wallet`` is used to pay and receive NBAI. Deposit for worker will be charged to this wallet,
    and output from mining and doing task will be saved to this wallet.

        Please make sure you have the **private key** of this wallet for future usage.

    ``price_limit`` is recommended to keep as default.

    ``dual_mode`` controls ``mining when idle`` functionality.

        * When true, worker will mine NBAI when waiting for a task.

        * When false, worker will not mine NBAI when waiting for a task.

