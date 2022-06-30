# convert_product_export/ zencart
option_value_data['thumb_image'] = {
	'label': '',
	'url' : 'https://hokiglasszen.coded.co.nz/images/',
	'path' : to_str(option_value["attributes_image"]).replace(" ","%20"),
}

# check_product_import

option_list = convert['options']
	children_list = self.convert_option_to_child(option_list, convert)
	list_id =  duplicate_field_value_from_list(children_list,"id")
	ids = self.list_to_in_condition(list_id)
	r = self.select_raw("select * from migration_map where type = 'product_child' and id_src in " + ids)
	r = r['data']
	for child in children_list:
		row = get_row_from_list_by_field(r, 'code_src', child["code"])
		id_desc = row.get("id_desc")
		self.log(id_desc,"id_desc")

		config_image_path = self._notice['target']['config']['image_product'].rstrip('/') if not self._notice['target'][
		'config'].get('site_id') else self._notice['target']['config']['image_product'].rstrip(
		'/') + '/sites/' + to_str(self._notice['target']['config']['site_id'])
		if child['thumb_image']['url'] or child['thumb_image']['path']:
			image_process = self.process_image_before_import(child['thumb_image']['url'],
															child['thumb_image']['path'])
			image_import_path = self.uploadImageConnector(image_process, self.add_prefix_path(
				self.make_woocommerce_image_path(image_process['path']), config_image_path))

			if image_import_path:
				product_image = self.remove_prefix_path(image_import_path,
									self._notice['target']['config']['image_product'])
				_, image_details = self.get_sizes(image_process['url'])
				thumbnail_id = self.wp_image(product_image, image_details, child['thumb_image'].get('label', ''))

				self.log(thumbnail_id,"thumbnail_id1")
				product_meta = {
					'meta_value': thumbnail_id,
				}
				where={
				'post_id': id_desc,
				'meta_key':"_thumbnail_id"

				}
				update_query = self.import_data_connector(self.create_update_query_connector("postmeta", product_meta, where))
