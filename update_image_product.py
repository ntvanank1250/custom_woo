product_id=self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
if product_id:
    config_image_path = self._notice['target']['config']['image_product'].rstrip('/') if not self._notice['target'][
    'config'].get('site_id') else self._notice['target']['config']['image_product'].rstrip(
    '/') + '/sites/' + to_str(self._notice['target']['config']['site_id'])
    if convert['thumb_image']['url'] or convert['thumb_image']['path']:
        image_process = self.process_image_before_import(convert['thumb_image']['url'],
                                                        convert['thumb_image']['path'])
        image_import_path = self.uploadImageConnector(image_process, self.add_prefix_path(
            self.make_woocommerce_image_path(image_process['path']), config_image_path))

        if image_import_path:
            product_image = self.remove_prefix_path(image_import_path,
                                                    self._notice['target']['config']['image_product'])
            _, image_details = self.get_sizes(image_process['url'])
            thumbnail_id = self.wp_image(product_image, image_details, convert['thumb_image'].get('label', ''))

            self.log(thumbnail_id,"thumbnail_id1")
            product_meta = {
                'meta_value': thumbnail_id,
            }
            where={
            'post_id': product_id,
            'meta_key':"_thumbnail_id"

            }
            update_query = self.import_data_connector(self.create_update_query_connector("postmeta", product_meta, where))
