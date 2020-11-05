# Facture

::: sender
### $sender.name$  
$sender.address_part_1$  
$sender.address_part_2$  
$sender.phone$  
<$sender.email$>  
SIREN: $sender.siren$  
:::


::: receiver
### $receiver.name$
$receiver.address_part_1$  
$receiver.address_part_2$  
:::

::: number
*Facture n° $number$*
:::

::: date
Fait le $date$
:::

| Quantité | Désignation                             | Prix unitaire HT     | Prix total HT     |
| -------- | --------------------------------------- | -------------------- | ----------------- |
$for(products)$
| $products.quantity$ | $products.description$ | $products.unitary_price$ | $products.total_price$ |
$endfor$
|||                                                         **Total HT (en €)** | $total_price$ |

::: right
*TVA non applicable, art. 293 B du CGI*
:::

::: bank
**Coordonnées bancaires:**  
Titulaire du compte : $bank_details.name$  
Banque : $bank_details.bank$  
IBAN : $bank_details.iban$  
CODE BIC : $bank_details.bic$
:::

::: little-conditions
Conditions de paiement : paiement à réception de facture à 30 jours.  
Indemnité forfaitaire pour frais de recouvrement due au créancier en cas de retard de paiement: 40€
:::
