select * from (corgi_store_listing join corgi_store_corgi on corgi_store_listing.corgi_id=corgi_store_corgi.id) 
    where corgi_store_listing.open=1 and
        gender='M' and
        coloring='Red-Headed Tricolor' and
        state ='AZ' and
        age < 3
        price >= 1000 and
        price <= 2000;
