# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('donation', '0086_update_donation_view'),
    ]

    operations = [migrations.RunSQL("""
    DROP VIEW IF EXISTS donation_donationcomponent;

    CREATE VIEW donation_donationcomponent AS
(select *, t.amount - t.fees as amount_net from
        (select
          row_number()
          over ()                                                 as id,
          component.id                                            as pledge_component_id,
          d.id                                                    as donation_id,
          d.amount * component.amount / total_amount              as amount,
          coalesce(pin.fees * component.amount / total_amount, 0) + coalesce(stripe.fees * component.amount / total_amount, 0) as fees
        from donation_pledgecomponent as component
          join (select
                  pledge_id,
                  sum(amount) as total_amount
                from donation_pledgecomponent
                group by pledge_id) as total_per_pledge
            on component.pledge_id = total_per_pledge.pledge_id
          join donation_donation as d
            on d.pledge_id = total_per_pledge.pledge_id
          left join pinpayments_pintransaction as pin
            on pin.id = d.pin_transaction_id
          left join donation_stripetransaction as stripe
            on stripe.id = d.stripe_transaction_id) t);
    """,
                                    reverse_sql="""
                                    DROP VIEW IF EXISTS donation_donationcomponent;
                                    """)
                  ]
