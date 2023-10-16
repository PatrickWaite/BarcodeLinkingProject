def get_barcodeData(barcode):
    query = f"""
select 
it.barcode,
hrt.call_number,
it.volume as "Volume/Description",
it.effective_shelving_order, 
inst.title,
lt."name" as "Collection Location",
lct."name" as "Campus",
mtt."name" as "material_type",
it.status__name as "item status",
string_agg(distinct itn2.notes__note,', ') as "Item Notes",
string_agg(distinct hrtn.notes__note,', ') as "Holding Notes",
string_agg(distinct itn.notes__note, ', ') as "Instance Notes",
string_agg(distinct itcn.circulation_notes__note,', ') as "Circulation Notes",
string_agg(distinct itan.administrative_notes,', ') as "Administrative Notes",
string_agg(distinct sct."name",', ') as "Statistical Code",
it.hrid as "Item HRID",
hrt.hrid as "Holding Record HRID",
inst.hrid as "Instance HRID",
it.metadata__updated_date as "Item Metadata Updated",
hrt.metadata__updated_date as "Holding Record Metadata Updated",
inst.metadata__updated_date as "Instance Metadata Updated"
from 
inventory.item__t it 
left outer join inventory.item__t__circulation_notes itcn on itcn.hrid = it.hrid 
left outer join inventory.item__t__notes itn2 on itn2.hrid = it.hrid
left outer join inventory.item__t__administrative_notes itan on itan.hrid = it.hrid 
left outer join inventory.item__t__statistical_code_ids itsci on itsci.hrid = it.hrid 
left outer join inventory.statistical_code__t sct on sct.id = itsci.statistical_code_ids 
join inventory.holdings_record__t hrt on hrt.id = it.holdings_record_id
left outer join inventory.holdings_record__t__notes hrtn on hrtn.hrid = hrt.hrid 
--join inventory.holdings_record__t__notes hrtn on hrtn.id = hrt.id 
join inventory.instance__t inst on inst.id = hrt.instance_id 
left outer join inventory.instance__t__notes itn on itn.hrid = inst.hrid
join inventory.material_type__t mtt on mtt.id = it.material_type_id
join inventory.location__t lt on lt.id = hrt.effective_location_id 
join inventory."loc-campus__t" lct on lct.id = lt.campus_id 
where 
it.barcode IN ({barcode})
--'barcode'
--lct.code = 'UM' or lct.code = 'RP'
group by 1,
it.barcode, 
inst.title, 
hrt.call_number,
hrt.effective_location_id,
lt."name",
it.status__name,
it.volume, 
mtt."name",
it.hrid,
lct."name",
inst.hrid,
hrt.hrid,
it.effective_shelving_order,
it.metadata__updated_date,
hrt.metadata__updated_date,
inst.metadata__updated_date 
    """
    return query